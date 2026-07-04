import ast
import json
import subprocess
import numpy as np
from django.utils import timezone
from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from storage.models import UserModel
from .utils import (
    ensure_docker_image,
)
@login_required
@never_cache
def home(request):
    if request.method == "GET" and 'simulacion_completa' in request.session:
        del request.session['simulacion_completa']
        
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
        container_name = f"simulation_{request.user.id}" 
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
            "valores_finales = {} \n"
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
            "import sys\n"
            "sys.stdout.write('==JSON_START==' + json.dumps(valores_finales) + '==JSON_END==')\n"
        )
        
        codigo_final = setup_numpy + code + extractor_json
        
        try:
            subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)
            
            resultado = subprocess.run([
                "docker", "run", "--rm", "-i",
                "--name", container_name,
                "--network", "none",
                "container", "python"
            ], input=codigo_final, capture_output=True, text=True, timeout=15)
            
            valores_reales = {}
            if resultado.returncode == 0:
                stdout_data = resultado.stdout
                if "==JSON_START==" in stdout_data and "==JSON_END==" in stdout_data:
                    try:
                        json_puro = stdout_data.split("==JSON_START==")[1].split("==JSON_END==")[0].strip()
                        valores_reales = json.loads(json_puro)
                    except json.JSONDecodeError:
                        pass
            else:
                error_script = resultado.stderr if resultado.stderr else "Error de ejecución."
                return render(request, 'simulator/home.html', {'error': f"Error en tu script: {error_script}"})

            input_data,output_data,tree = {},{},ast.parse(code)
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
         
            request.session['modelo']= code
            request.session['simulacion_completa'] = json_unificado
            return redirect('simulator')
            
        except subprocess.TimeoutExpired:
            return render(request, 'simulator/home.html', {'error': 'La simulación fue abortada por exceder el tiempo límite.'})
            
        except subprocess.CalledProcessError as e:
            return render(request, 'simulator/home.html', {'error': f"Error crítico: {e}"})
            
        finally:
            subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)
    
    return render(request, 'simulator/home.html', {})

@login_required
@never_cache
def simulator(request):
    datos_sesion = request.session.get('simulacion_completa', None)
    model = request.session.get('modelo',None)
    datos_json_string = json.dumps(datos_sesion) if datos_sesion else None
    return render(request, 'simulator/simulator.html', {
        'json_simulacion': datos_json_string,
        'modelo':model,
    })
    
    
@login_required
@never_cache
def save_model(request):
    if request.method == "POST":
        codigo_texto = request.POST.get('code')
        if codigo_texto:
            nombre_archivo = "modelo.py"
            archivo_final = ContentFile(codigo_texto.strip().encode('utf-8'))
            archivo_final.name = nombre_archivo
            usermodel = UserModel(
                user = request.user,
                name = nombre_archivo,
                file = archivo_final,
                first_date = timezone.now().date(),
                last_date = timezone.now().date()
            )
            usermodel.save()
        return redirect('simulator')
    return redirect('home')

@login_required
@never_cache
def stop_model(request):
    if request.method == "POST":
        request.session.pop('simulacion_completa', None)
        request.session.pop('modelo_codigo', None)
        request.session.pop('modelo_nombre', None)
        return redirect('home')
        
    return redirect('simulator')