import pandas as pd
import h2o
import os
import unicodedata
import numpy as np
import discretizacion as dz
import subprocess
import ImageDef as img
from h2o.estimators.random_forest import H2ORandomForestEstimator
from IPython.display import Image

class ArbolZipa():
    def __init__(self):
        self.listaVarDis=["T"]
        self.test=h2o.H2OFrame()
        self.valoresDeT=[]
        self.discretizador=dz.discretizador()
        #self.dz=discretizacion()
        self.rf_v2 = H2ORandomForestEstimator(
            model_id="modelo arbol",
            ntrees=200,
            stopping_rounds=2,
            stopping_tolerance=0.2,
            score_each_iteration=True,
            max_depth=200,
            sample_rate=0.6,
            seed=56478)

    def variables(self,df):
        data = pd.DataFrame(columns=("Transversales_desarrollo","Puntos Codificación","T","valor_indicador_ans_desarrollo",
        "valor_indicador_ejecucion_desarrollo","Pila_desarrollo","Categoría","Web Service",
        "Base de datos","Reporte","Aplicación de escritorio","Subsistema"))
        variables={"Transversales_desarrollo","Puntos Codificación","T","valor_indicador_ans_desarrollo",
        "valor_indicador_ejecucion_desarrollo","Pila_desarrollo","Categoría","Web Service",
        "Base de datos","Reporte","Aplicación de escritorio","Subsistema"}
        for i in variables:
            try:
                data[i]=df[i]
            except:
                pass
        return data

    def crear_arbol(self):
        
        try:
            h2o.shutdown(prompt=False)
        except:
            pass
        json={}
        h2o.init(max_mem_size = "2G")
        h2o.remove_all() 
        df = pd.read_excel('Excel_Corregido_Final.xlsx',encoding="ISO-8859-1")
        df=self.variables(df)
        umbrales =np.linspace(0, 1, 7)
        df = df.replace(np.nan, -1)
        df = df.replace({'Categoría':{'a':'a','é':'e','í':'i','ó':'o','ú':'u'}}, regex=True)
        print(df["Categoría"])
        covtype_df=h2o.H2OFrame(self.discretizador.discretizar(self.listaVarDis,umbrales,df))
        covtype_df=covtype_df.drop([0], axis=0)
        print("ojo acá")
        print(self.discretizador.listaDeIntervalos)
        covtype_df["T"]=covtype_df["T"].asfactor()
        df=covtype_df
        t=covtype_df["T"]
        covtype_df=covtype_df.drop(["T"],axis=1)
        covtype_df["T"] = t["T"]
        self.test=covtype_df.drop(["T"],axis=1)
        train,x = covtype_df.split_frame([0.8], seed=56478)
        valid,x=covtype_df.split_frame([0.5],seed=56478)
        #self.test=self.test.drop(["T"],axis=1)
        covtype_X = covtype_df.col_names[:-1]     
        covtype_y = covtype_df.col_names[-1] 
        self.rf_v2.train(x=covtype_X, y=covtype_y, training_frame=train,validation_frame=valid)
        json["val"]=1-self.rf_v2.mean_per_class_error(valid=True)
        print(self.rf_v2.confusion_matrix(valid))
        # json["matriz"]=self.rf_v2.confusion_matrix(valid).as_data_frame().to_numpy()
        # json["matriz"]=json["matriz"].tolist()
        # for i in json["matriz"]:
        #     i[len(i)-2]=round(i[len(i)-2],4)
        print(json["val"])
        # json["val"]=self.rf_v2.mean_per_class_error(valid=True)
        #json_string = json.dumps(str(self.rf_v2._get_metrics),ensure_ascii=False)
        #python_dictionary = json.loads(json_string)
        #print(python_dictionary)
        print("algo")

    def dibujarArbol(self):
        mojo_file_name = "ModeloMojo.zip"
        h2o_jar_path = r"C:\Users\yrios\AppData\Local\Programs\Python\Python37\Lib\site-packages\h2o\backend\bin\h2o.jar"
        mojo_full_path = mojo_file_name
        gv_file_path = "Modelo.gv"
        image_file_name = "Arbol_Dec_Zipa"
        self.rf_v2.download_mojo(mojo_file_name)
        img.generateTree(h2o_jar_path, mojo_full_path, gv_file_path, image_file_name, 3)
        img.generateTreeImage(gv_file_path, image_file_name, 3)

    def entrenamiento(self,opcion,archivo):
        json={}
        if opcion=="archivoLocal":
            self.crear_arbol()
        else:
            df = pd.read_excel(archivo,encoding="ISO-8859-1")
            umbrales =np.linspace(0, 1, 7)
            df = df.replace(np.nan, -1)
            df = df.replace({'Categoría':{'a':'a','é':'e','í':'i','ó':'o','ú':'u'}}, regex=True)
            covtype_df=h2o.H2OFrame(self.discretizador.discretizar(self.listaVarDis,umbrales,df))
            covtype_df=covtype_df.drop([0], axis=0)
            covtype_df["T"]=covtype_df["T"].asfactor()
            train,x = covtype_df.split_frame([0.8], seed=56478)
            valid,x=covtype_df.split_frame([0.5],seed=56478)
            covtype_X = covtype_df.col_names[:-1]     
            covtype_y = covtype_df.col_names[-1] 
            self.rf_v2.train(x=covtype_X, y=covtype_y, training_frame=train,validation_frame=valid)
            
            
    
    def obtener_indicadores(self,df,nombre):
        indicadorANS=0
        indicadorEjecusion=0
        nombre=unicodedata.normalize('NFKD', nombre).encode('ASCII', 'ignore')
        for i in range(len(df["ingeniero"])):
            n=unicodedata.normalize('NFKD', df["ingeniero"][i]).encode('ASCII', 'ignore')
            if n==nombre:
                
                try :
                    indicadorANS=int(df["valor_indicador_ans"][i])
                except:
                    pass
                try:
                    indicadorEjecusion=int(df["valor_indicador_ejecucion"][i])
                except:
                    pass
        return indicadorANS,indicadorEjecusion
    
    def obtener_variables(self,df,nombre):
        transversales=0
        pila=0
        nombre=unicodedata.normalize('NFKD', nombre).encode('ASCII', 'ignore')
        for i in range(len(df["Responsable Desarrollo"])):
            n=unicodedata.normalize('NFKD', ["Responsable Desarrollo"][i]).encode('ASCII', 'ignore')
            if n==nombre:
                transversales=df["Transversales"][i]
                pila=df["Pila"][i]
        return transversales,pila

    def predecir(self, variables):
        json={
            "Puntos Codificación":[variables["PuntosCodificación"]],
            "Categoría":[variables["Categoría"]],
            "Web Service":[variables["webService"]],
            "Base de datos":[variables["basedatos"]],
            "Reporte":[variables["reporte"]],
            "Aplicación de escritorio":[variables["aplicacionDeEscritorio"]],
            "Subsistema":[variables["SusbSistema"]]
        }
        dftemporal=pd.read_excel("C://Users//yrios//source//repos//zipa-repositorios//Excel//indicadores_ingenieros02.xlsx")
        indicadorANS,indicadorEjecusion=self.obtener_indicadores(dftemporal,variables["nombre"])
        json["valor_indicador_ans_desarrollo"]=[indicadorANS]
        json["valor_indicador_ejecucion_desarrollo"]=[indicadorEjecusion]
        dftemporal=pd.read_excel("C://Users//yrios//source//repos//zipa-repositorios//Excel//conocimiento_encuesta.xlsx")
        transversales,pila=self.obtener_variables(dftemporal,variables["nombre"])
        json["Transversales_desarrollo"]=[transversales]
        json["Pila_desarrollo"]=[pila]
        print(json)
        test=pd.DataFrame.from_dict(json)
        test = test.replace(np.nan, None)
        print(test)
        dftest=h2o.H2OFrame(test)
        dftest=dftest.drop([0],axis=0)
        final_rf_predictions = self.rf_v2.predict(dftest[:-1])
        df_predict=final_rf_predictions.as_data_frame(use_pandas=True)
        
        nuevaColumna=self.discretizador.getIntervalo(self.discretizador.get_valT(),df_predict["predict"])
        aux=nuevaColumna[0].replace("(","").replace(")","").split(",")
        print(aux)
        nuevaColumna=pd.DataFrame(nuevaColumna)
        nuevaColumna = nuevaColumna.rename(columns = {0: 'T'})
        nuevaColumna=h2o.H2OFrame(nuevaColumna)
        dftest["t"] = nuevaColumna["T"]
        

if __name__ =="__main__":
    arbol=ArbolZipa()
    arbol.crear_arbol()
    arbol.dibujarArbol()
    json={
            "Categoría": "Nueva funcionalidad",
            "Pila_desarrollo": 0,
            "PuntosCodificación": 1,
            "SusbSistema": "Servicios Financieros",
            "Transversales": 0,
            "aplicacionDeEscritorio": 5,
            "basedatos": 2,
            "nombre": "Edwar Fernando Gomez Serna",
            "reporte": 4,
            "valor_indicador_ans_desarrollo": 0,
            "valor_indicador_ejecucion_desarrollo": 0,
            "webService": 3
        }
    arbol.predecir(json)
    arbol.entrenamiento("","p18.xlsx")
    
    