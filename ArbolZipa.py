import pandas as pd
import h2o
import os

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

    def crear_arbol(self):
        
        h2o.init(max_mem_size = "2G")
        h2o.remove_all() 
        df = pd.read_excel('p18.xlsx',encoding="ISO-8859-1")
        umbrales =np.linspace(0, 1, 7)
        df = df.replace(np.nan, None)
        covtype_df=h2o.H2OFrame(self.discretizador.discretizar(self.listaVarDis,umbrales,df))
        covtype_df=covtype_df.drop([0], axis=0)
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

    def dibujarArbol(self):
        mojo_file_name = "ModeloMojo.zip"
        h2o_jar_path = "C:/Users/yulea/AppData/Local/Programs/Python/Python36/Lib/site-packages/h2o/backend/bin/h2o.jar"
        mojo_full_path = mojo_file_name
        gv_file_path = "C:/Users/yulea/Documents/pruebasPY/Modelo.gv"
        image_file_name = "c:/Users/yulea/Documents/pruebasPY/Arbol_Dec_Zipa"
        self.rf_v2.download_mojo(mojo_file_name)
        img.generateTree(h2o_jar_path, mojo_full_path, gv_file_path, image_file_name, 3)
        img.generateTreeImage(gv_file_path, image_file_name, 3)

    def entrenamiento(self,opcion,archivo):
        if opcion=="archivoLocal":
            self.crear_arbol()
        else:
            df = pd.read_excel(archivo,encoding="ISO-8859-1")
            umbrales =np.linspace(0, 1, 7)
            df = df.replace(np.nan, None)
            covtype_df=h2o.H2OFrame(self.discretizador.discretizar(self.listaVarDis,umbrales,df))
            covtype_df=covtype_df.drop([0], axis=0)
            covtype_df["T"]=covtype_df["T"].asfactor()
            train,x = covtype_df.split_frame([0.8], seed=56478)
            valid,x=covtype_df.split_frame([0.5],seed=56478)
            covtype_X = covtype_df.col_names[:-1]     
            covtype_y = covtype_df.col_names[-1] 
            self.rf_v2.train(x=covtype_X, y=covtype_y, training_frame=train,validation_frame=valid)


    def predecir(self,test):
        print(test)
        print("________________________________________________________________________________________________________________")
        final_rf_predictions = self.rf_v2.predict(test[:-1])
        df_predict=final_rf_predictions.as_data_frame(use_pandas=True)
        print(self.discretizador.get_valT())
        nuevaColumna=self.discretizador.getIntervalo(self.discretizador.get_valT(),df_predict["predict"])
        nuevaColumna=pd.DataFrame(nuevaColumna)
        nuevaColumna = nuevaColumna.rename(columns = {0: 'T'})
        print(nuevaColumna)
        nuevaColumna=h2o.H2OFrame(nuevaColumna)
        #self.test=self.test.as.data_frame(use_pandas=True)

        test["t"] = nuevaColumna["T"]
        print(test)

if __name__ =="__main__":
    arbol=ArbolZipa()
    arbol.crear_arbol()
    arbol.dibujarArbol()
    test=pd.read_excel('p18.xlsx',encoding="ISO-8859-1")
    test = test.replace(np.nan, None)
    dftest=h2o.H2OFrame(test)
    dftest=dftest.drop([0],axis=1)
    dftest=dftest.drop([0],axis=0)
    print(dftest)
    dftest=dftest.drop(["T"],axis=1)
    print(dftest)
    arbol.predecir(dftest)
    arbol.entrenamiento("","p18.xlsx")
    