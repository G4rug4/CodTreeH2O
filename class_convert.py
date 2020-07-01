import json
import base64
import pydotplus
import pygraphviz as pgv
from PIL import Image
import h2o
import ImageDef as id

#from graphviz import Source
#h2o.init()
mojo_file_name = "ModeloMojo.zip"
h2o_jar_path = "C:/Users/yulea/AppData/Local/Programs/Python/Python36/Lib/site-packages/h2o/backend/bin/h2o.jar"
mojo_full_path = mojo_file_name
gv_file_path = "C:/Users/yulea/Documents/pruebasPY/my_gbm_graph2.gv"
image_file_name = "c:/Users/yulea/Documents/pruebasPY/my-image"

try:
    with(open(gv_file_path)) as lines:
        archivo=open("C:/Users/yulea/Documents/pruebasPY/my_gbm_graph3.gv","w",encoding="utf-8")
        for line in lines:
            if line.find("<0xF3>")!=-1 or line.find("Ã³") !=-1:
                print (line)
                line=line.replace("<0xF3>","ó")
                line=line.replace("Ã³","ó")
                archivo.write(line)
            elif line.find("<0xED>")!=-1 or line.find("Ã­") !=-1:
                print (line)
                line=line.replace("<0xED>","í")
                line=line.replace("Ã­","í")
                archivo.write(line)
            elif line.find("<0xE9>")!=-1:
                print (line)
                line=line.replace("<0xE9>","é")
                archivo.write(line)
            elif line.find("[NA]")!=-1:
                print (line)
                line=line.replace("[NA]","valor nulo")
                archivo.write(line)
            else:
                archivo.write(line)
        archivo.close()

except:
    print("la cagamos")
    pass
G=pgv.AGraph("C:/Users/yulea/Documents/pruebasPY/my_gbm_graph3.gv")
G.edge_attr['color']='#4cba4b'
G.node_attr['style']='filled,setlinewidth(0)'
G.node_attr['fillcolor']="#ff861d"
print("-----------------------------------------------------------------------------------------------------------------------------")
#nodo=G.get_subgraph(name="cluster_0")

#print(nodo.get_name())
print(G.subgraphs())


for subgrafo in G.subgraphs():
    #nodo=G.get_subgraph(nombre.get_name())
    print(subgrafo.get_name())
    subgrafo.layout() # default to neato
    subgrafo.layout(prog='dot') # use dot
    subgrafo.draw('C:\\Users\\yulea\\Documents\\pruebasPY\\'+subgrafo.get_name()+'.png')

# no=nodo.get_node('SG_0_Node_31')
# no.attr['fillcolor']="#ff8c00"
nodo.layout() # default to neato
nodo.layout(prog='dot') # use dot
nodo.draw('C:\\Users\\yulea\\Documents\\pruebasPY\\file.png')
img = Image.open('C:\\Users\\yulea\\Documents\\pruebasPY\\file.png')
img.show()
print(nodo.nodes())
print("-----------------------------------------------------------------------------------------------------------------------------")

#nodo.node_attr['color']='green'
#file=G.render(filename='img.png')


