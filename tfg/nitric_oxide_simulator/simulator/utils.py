import subprocess
import uuid
import re
import os
import json
import re
from django.shortcuts import render, redirect
from django.conf import settings
import ast

def simulation_inform_generator(file):
    print(file.name)
    print(file.size)
    if file.size > 2000000  or  not file.name.endswith('.py'):
        print("This file can't execute in this app")
    else:
        print("This file can execute in this app")
  



def revise_file(file):
    print(file.name)
    print(file.size)
    
    # Revise format and size
    if file.size > 2000000  or  not file.name.endswith('.py'):
        print("This file can't execute in this app")
    else:
        print("This file can execute in this app")
    
    # Revise  
    dangerous_command =["exec"]
    dangrerous_library = ["subprocess","ast","os","utils"]
    return True

  
        



def ensure_docker_image():
    """Verifica si la imagen existe, y si no, la construye usando el Dockerfile local."""
    try:
        resultado = subprocess.run(
            ["docker", "image", "inspect", "dockerfile"], 
            capture_output=True, text=True
        )
        if resultado.returncode != 0:
            ruta_proyecto = settings.BASE_DIR
            subprocess.run(["docker", "build", "-t", "dockerfile", str(ruta_proyecto)], check=True)
    except subprocess.CalledProcessError as e:
        print(" Error al intentar generar la imagen desde el Dockerfile:", e)


def extract_variables_models(contenido_texto):
    """Busca dinámicamente dimensiones (rowN_, columnN_, depthN_) y tiempos en el main."""
    datos_inicio = {}
    match_main = re.search(r'if __name__\s*==\s*["\']__main__["\']\s*:(.*)', contenido_texto, re.DOTALL)
    if not match_main:
        return datos_inicio
        
    bloque_main = match_main.group(1)
    
    for var_name in ['rowN_', 'columnN_', 'depthN_','N_']:
        match = re.search(r'\b' + var_name + r'\s*=\s*(\d+)', bloque_main)
        if match:
            datos_inicio[var_name] = int(match.group(1))
            
    match_tiempos = re.search(r'start_t\s*,\s*end_t\s*,\s*delta_t\s*=\s*([\d\.\s,]+)', bloque_main)
    if match_tiempos:
        valores = [float(v.strip()) for v in match_tiempos.group(1).split(',')]
        if len(valores) >= 3:
            datos_inicio["start_t"] = valores[0]
            datos_inicio["end_t"] = valores[1]
            datos_inicio["delta_t"] = valores[2]
            
    return datos_inicio

def clean_numpy_data(salida_cruda):
    """Extrae el eje de tiempo y junta todo el chorro numérico de C de forma plana."""
    limpio = salida_cruda.replace('\n', ' ').replace('\r', ' ')
    limpio = re.sub(r'\s+', ' ', limpio).strip()
    
    bloques = re.findall(r'\[[\d\s\.\-\+e:...]+\]', limpio)
    eje_tiempo = []
    valores_numericos = []
    
    if len(bloques) >= 2:
        for x in bloques[0].replace('[','').replace(']','').split():
            if '...' not in x:
                try: eje_tiempo.append(float(x))
                except ValueError: pass
                
        texto_completo_c = " ".join(bloques[1:])
        for x in texto_completo_c.replace('[','').replace(']','').split():
            if '...' not in x:
                try: valores_numericos.append(float(x))
                except ValueError: pass
                
    return eje_tiempo, valores_numericos
