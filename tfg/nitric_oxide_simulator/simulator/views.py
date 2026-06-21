import subprocess
import random
import re
import os
import json
import re
from django.shortcuts import render, redirect
from django.conf import settings
from .utils import ensure_docker_image,extract_variables_models,clean_numpy_data,revise_file

def home(request):
    if request.method == "POST" and request.FILES.getlist('file'):
        files = request.FILES.getlist('file')
        print(" Listado de ficheros")
        # Revisar cada uno
        for file in files:
            if revise_file(file) == False:
                 return render(request, 'simulator/home.html', {})
        
        ensure_docker_image()
        container_name = f"simulation_{request.user.id}" 
        subprocess.run([
                "docker", "run", "-d", 
                "--name", container_name, 
                "dockerfile", 
                "sh", "-c", "mkdir -p /app && tail -f /dev/null"
            ], check=True)       
        try:
          
            variables = {} 
            for file in files:
                if file.name.endswith('.py'):
                    script_code = file.read().decode('utf-8')
                    variables = extract_variables_models(script_code)
                    file.seek(0)
            
           
            
            for f in files:
                contenido_archivo = f.read()
                subprocess.run([
                    "docker", "exec", "-i", 
                    container_name, 
                    "sh", "-c", f"cat > /app/{f.name}"
                ], input=contenido_archivo, check=True)
            
            script_a_ejecutar = next((f.name for f in files if f.name.endswith('.py')), None)            
            if script_a_ejecutar:
                comando_inyectado = (
                    f"import numpy as np; "
                    f"np.set_printoptions(threshold=np.inf); "
                    f"import sys; "
                    f"sys.argv=['{script_a_ejecutar}']; "
                    f"exec(open('{script_a_ejecutar}').read())"
                )

                resultado = subprocess.run([
                    "docker", "exec", 
                    "-w", "/app", 
                    container_name, 
                    "python", "-c", comando_inyectado
                ], capture_output=True, text=True)
                
                salida_consola = resultado.stdout.strip()
                errores_consola = resultado.stderr.strip()

                if salida_consola:
                    t_lista, c_valores = clean_numpy_data(salida_consola)
                    json_unificado = {
                        "initial_data": variables,  
                        "final_results": {
                            "time": t_lista,
                            "concentration": c_valores  
                        }
                    }                    
                    request.session['simulacion_completa'] = json_unificado
                    return redirect('simulator')
                    
                elif errores_consola:
                    error_msg = f"Error en la simulación: {errores_consola}"
            else:
                error_msg = "No se subió ningún script .py"

        except subprocess.CalledProcessError as e:
            error_msg = f"Error crítico de Docker: {e}"
        finally:
            subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)
    return render(request, 'simulator/home.html', {})

def simulator(request):
    datos_sesion = request.session.get('simulacion_completa', None)
    datos_json_string = json.dumps(datos_sesion) if datos_sesion else None
    return render(request, 'simulator/simulator.html', {
        'json_simulacion': datos_json_string
    })
