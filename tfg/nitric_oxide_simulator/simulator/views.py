import subprocess
import random
import re
import os
import json
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from django.conf import settings
from .utils import ensure_docker_image,extract_variables_models,clean_numpy_data,revise_file
from storage.models import UserModel
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
import subprocess

def home(request):
    files = []
    if request.method == "GET" and 'archivo_modelo_id' in request.session:
        modelo_id = request.session.get('archivo_modelo_id')
        instancia_modelo = get_object_or_404(UserModel, id=modelo_id, user=request.user)        
        
        archivo_emulado = ContentFile(instancia_modelo.file.read())
        nombre_seguro = instancia_modelo.name.replace(" ", "_")
        archivo_emulado.name = nombre_seguro if nombre_seguro.endswith('.py') else f"{nombre_seguro}.py"
        
        files.append(archivo_emulado)
        del request.session['archivo_modelo_id'] 
    elif request.method == "POST" and request.FILES.getlist('file'):
        files = request.FILES.getlist('file')
        for file in files:
            if revise_file(file) == False:
                return render(request, 'simulator/home.html', {'error': 'Archivo no válido'})
    if files:
        print("Listado de ficheros procesando...")
        ensure_docker_image()
        container_name = f"simulation_{request.user.id}" 
        
        try:
            subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)
            subprocess.run([
                "docker", "run", "-d", 
                "--name", container_name, 
                "dockerfile", 
                "sh", "-c", "mkdir -p /app && tail -f /dev/null"
            ], check=True)       
            
            variables = {} 
            for file in files:
                if file.name.endswith('.py'):
                    script_code = file.read().decode('utf-8')
                    variables = extract_variables_models(script_code)
                    file.seek(0)
            
            for f in files:
                contenido_archivo = f.read()
                nombre_destino = f.name.replace(" ", "_")
                subprocess.run([
                    "docker", "exec", "-i", 
                    container_name, 
                    "sh", "-c", f"cat > /app/{nombre_destino}"
                ], input=contenido_archivo, check=True)
            
            script_a_ejecutar = next((f.name.replace(" ", "_") for f in files if f.name.endswith('.py')), None)            
            if script_a_ejecutar:
                # Usamos comillas triples por si acaso
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
                    return render(request, 'simulator/home.html', {'error': error_msg})
            else:
                error_msg = "No se detectó ningún script .py válido"
                return render(request, 'simulator/home.html', {'error': error_msg})

        except subprocess.CalledProcessError as e:
            error_msg = f"Error crítico de Docker: {e}"
            return render(request, 'simulator/home.html', {'error': error_msg})
            
        finally:
            subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)

    return render(request, 'simulator/home.html', {})
def simulator(request):
    datos_sesion = request.session.get('simulacion_completa', None)
    datos_json_string = json.dumps(datos_sesion) if datos_sesion else None
    return render(request, 'simulator/simulator.html', {
        'json_simulacion': datos_json_string
    })
