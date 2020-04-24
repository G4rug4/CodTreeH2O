import pandas as pd

class discretizador():

    def __init__(self):
        self.valoresDeT=[]
        self.cuantiles=[]
    
    def discretizar(self,listaVarDis,umbrales,df):
        for variable in listaVarDis:
            try:
                vector2=[]
                vector=[]
                vector=self.create_num_vector(df, variable)
                self.cuantiles =self.get_quantile(vector, umbrales)
                vector2=self.nuevaColumna(vector,self.cuantiles)
                if variable=="T":
                    self.valoresDeT=self.cuantiles
                if vector2:
                    df[[variable]] = pd.DataFrame(vector2).rename(columns = {0: variable})
            except:
                pass
        
        return df
    
    def create_num_vector(self,df, variable):
        num_vector = df[variable]
        if num_vector.dtype == 'O':
            num_vector = num_vector.str.replace(",", ".")
            num_vector = num_vector.str.replace(" ", "")
        return pd.to_numeric(num_vector)

    def get_quantile(self,num_vector, umbrales):
        q_vect = []
        for i in umbrales:
            q_vect = q_vect + [round(num_vector.quantile(i),4)]
            q_vect = list(set(q_vect))
            q_vect.sort() 
        return q_vect

    def nuevaColumna(self,vector,cuantiles):
        nuevoVector=[]
        listaIntervalos=[]
        #Construcción de una arreglo de tuplas con los intervalos de discreción 
        for i in range(len(cuantiles)-1):
            if(i ==0):
                listaIntervalos.append((0,cuantiles[i+1]))
            else:
                listaIntervalos.append((cuantiles[i],cuantiles[i+1]))
        print("lista de intervalos")
        print(listaIntervalos)
        for i in range(len (vector)):
            for j in range(len(listaIntervalos)):
                if vector[i]<=listaIntervalos[j][1] and vector[i]>=listaIntervalos[j][0]:
                    nuevoVector.append(str(j))
        print("nuevo vector")
        print(nuevoVector)
        
        return nuevoVector

    def getIntervalo(self,cuantiles,predictions):
        nuevaColumna2=[]
        listaIntervalos=[]
        for i in range(len(cuantiles)-1):
            if(i ==0):
                listaIntervalos.append((0,cuantiles[i+1]))
            else:
                listaIntervalos.append((cuantiles[i],cuantiles[i+1]))
        for i in predictions:
            nuevaColumna2.append(str(listaIntervalos[i]))
        return nuevaColumna2

    

    def get_valT(self):
        return self.valoresDeT

    