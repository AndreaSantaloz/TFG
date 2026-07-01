import ast
import json
import os
import random
import re
import subprocess
import types
import numpy as np

from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, redirect, render

from storage.models import UserModel
from .utils import (
    ensure_docker_image,
    
    
)

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
        
    elif request.method == "POST" and request.FILES.get('file'):
        model_file = request.FILES.get('file')
        if model_file.name.endswith('.py') and model_file.size < 2000000:
            files.append(model_file)
       
    if files:
        ensure_docker_image()
        container_name = f"simulation_{request.user.id}" 
        nombre_archivo_interno = "script.py"
        code = files[0].read().decode('utf-8')
        
        try:
            subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)
            subprocess.run([
                "docker", "run", "-d", 
                "--name", container_name, 
                "container", 
                "sh", "-c", "mkdir -p /app && tail -f /dev/null"
            ], check=True)
        
            files[0].seek(0)
            code = files[0].read().decode('utf-8')
            
            setup_numpy = (
                "import numpy as np\n"
                "try:\n"
                "    np.set_printoptions(threshold=np.inf)\n"
                "except:\n"
                "    pass\n"
            )
            
            extractor_json = (
                "\n\n"
                "import json\n"
                "import types\n"
                "import numpy as np\n"
                "valores_finales = {}\n"
                "for k, v in list(globals().items()):\n"
                "    if k.startswith('_') or k in ['json', 'types', 'np', 'valores_finales', 'k', 'v']:\n"
                "        continue\n"
                "    if isinstance(v, (types.ModuleType, types.FunctionType, types.BuiltinFunctionType)):\n"
                "        continue\n"
                "    try:\n"
                "        if isinstance(v, np.ndarray):\n"
                "            valores_finales[k] = v.tolist()\n"
                "        else:\n"
                "            json.dumps(v)\n"
                "            valores_finales[k] = v\n"
                "    except:\n"
                "        valores_finales[k] = str(v)\n"
                "\n"
                "with open('/app/variables.json', 'w') as f:\n"
                "    json.dump(valores_finales, f)\n"
            )
            
            codigo_final = setup_numpy + code + extractor_json
            subprocess.run([
                "docker", "exec", "-i",
                container_name,
                "sh", "-c", f"cat > /app/{nombre_archivo_interno}"
            ], input=codigo_final, check=True, text=True)
            
            resultado = subprocess.run([
                "docker", "exec", 
                "-w", "/app", 
                container_name, 
                "python", nombre_archivo_interno
            ], capture_output=True, text=True)
            
            resultado_json = subprocess.run([
                "docker", "exec", 
                container_name, 
                "cat", "/app/variables.json"
            ], capture_output=True, text=True)
            
            valores_reales = {}
            if resultado_json.returncode == 0:
                try:
                    valores_reales = json.loads(resultado_json.stdout)
                except json.JSONDecodeError:
                    pass

            input_data = {}
            output_data = {}
            tree = ast.parse(code)
            
            def revise_value_local(key, value, dictionary):
                if value is not None:
                    dictionary[key] = value

            for node in ast.walk(tree):
                if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                    for arg in node.value.args:
                        if isinstance(arg, ast.Name):
                            revise_value_local(arg.id, valores_reales.get(arg.id), input_data)
                        elif isinstance(arg, ast.Tuple): 
                            for el in arg.elts:
                                if isinstance(el, ast.Name):
                                    revise_value_local(el.id, valores_reales.get(el.id), input_data)
                                    
                    if isinstance(node.targets[0], ast.Tuple):
                        for item in node.targets[0].elts:
                            if isinstance(item, ast.Name):
                                revise_value_local(item.id, valores_reales.get(item.id), output_data)

            for output_var in list(output_data.keys()):
                if output_var in input_data:
                    del input_data[output_var]
            
            t_lista = output_data.get('t', [])
            c_valores = output_data.get('C', [])
            
            json_unificado = {
                "initial_data": input_data,  
                "final_results": {
                    "time": t_lista,
                    "concentration": c_valores  
                }
            }
            
            request.session['simulacion_completa'] = json_unificado
           
            
            return redirect('simulator')
            
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