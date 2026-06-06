import plotly.graph_objects as go
from TFG.catedra_mari_curi_ulpgc.main import TEST_compartmentalModelOfNitricOxide_1D
import numpy as np

# Añadir leyenda
# Añadir eje
"""
Gráficas 2d probadas
"""
def scatter_2d(x,y):
    fig= go.Figure()
    fig= fig.add_trace(go.Scatter(x=x,y=y,mode='markers'))
    fig.show()
    
def lines(x,y):
    fig= go.Figure()
    fig.add_trace(go.Scatter(x=x,y=y,mode='lines'))
    fig.show()
    
#Especificar la N usando las filas de concentracion 
def table_2d(x,y):
    column_names = ['Tiempo'] + ['Concentración']
    fig= go.Figure(data=[go.Table(
            header=dict(values=column_names),
            cells=dict(values=[x,y])
        )])
    fig.show()
    
"""
Gráficas 3d en desarrollo hasta poder probarlas
"""

def table_3d(x,y,z):
    column_names = ['Tiempo'] + ['Concentración']
    fig= go.Figure(data=[go.Table(
            header=dict(values=column_names),
            cells=dict(values=[x,y,z])
        )])
    fig.show()

def scatter_3d(x,y,z):
    fig= go.Figure()
    fig= fig.add_trace(go.Scatter(x=x,y=y,z=z,mode='markers'))
    fig.show()
    
def heatmap(x,y,z):
    fig= go.Figure()
    fig= fig.add_trace(go.Heatmap(x=x,y=y,z=z))
    fig.show()
    

    
#Falta heatmaps y graficas 3d (dos dimensiones(matriz de x columnas y 2/3 filas) y tres dimensiones(matriz de x columnas y 3/4 filas )) 
if __name__=="__main__":
    
    t,C=TEST_compartmentalModelOfNitricOxide_1D()
    for _i in range(0,C.shape[0]):
        if _i == 0:
            table_2d(t,C[_i])
            scatter_2d(t,C[_i])
            lines(t,C[_i])
    

    