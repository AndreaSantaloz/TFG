import subprocess
import uuid
import os
import json
import re
from django.shortcuts import render, redirect
from django.conf import settings

def asegurar_imagen_base():
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
        print("❌ Error al intentar generar la imagen desde el Dockerfile:", e)

import re

def extraer_variables_del_script(contenido_texto):
    """Busca dinámicamente dimensiones (rowN_, columnN_, depthN_) y tiempos en el main."""
    datos_inicio = {}
    match_main = re.search(r'if __name__\s*==\s*["\']__main__["\']\s*:(.*)', contenido_texto, re.DOTALL)
    if not match_main:
        return datos_inicio
        
    bloque_main = match_main.group(1)
    
    # Captura variables de dimensiones (da igual si faltan, por defecto serán 1)
    for var_name in ['rowN_', 'columnN_', 'depthN_']:
        match = re.search(r'\b' + var_name + r'\s*=\s*(\d+)', bloque_main)
        if match:
            datos_inicio[var_name] = int(match.group(1))
            
    # Captura la línea de tiempos (start_t, end_t, delta_t)
    match_tiempos = re.search(r'start_t\s*,\s*end_t\s*,\s*delta_t\s*=\s*([\d\.\s,]+)', bloque_main)
    if match_tiempos:
        valores = [float(v.strip()) for v in match_tiempos.group(1).split(',')]
        if len(valores) >= 3:
            datos_inicio["start_t"] = valores[0]
            datos_inicio["end_t"] = valores[1]
            datos_inicio["delta_t"] = valores[2]
            
    return datos_inicio

def limpiar_consola_numpy(salida_cruda):
    """Extrae el eje de tiempo y junta todo el chorro numérico de C de forma plana."""
    # Eliminamos saltos de línea molestos de la consola
    limpio = salida_cruda.replace('\n', ' ').replace('\r', ' ')
    limpio = re.sub(r'\s+', ' ', limpio).strip()
    
    # Capturamos los bloques numéricos encerrados en corchetes
    bloques = re.findall(r'\[[\d\s\.\-\+e:...]+\]', limpio)
    eje_tiempo = []
    valores_numericos = []
    
    if len(bloques) >= 2:
        # El primer bloque grande es el eje de tiempo 't'
        for x in bloques[0].replace('[','').replace(']','').split():
            if '...' not in x:
                try: eje_tiempo.append(float(x))
                except ValueError: pass
                
        # Los bloques siguientes corresponden a la matriz C
        texto_completo_c = " ".join(bloques[1:])
        for x in texto_completo_c.replace('[','').replace(']','').split():
            if '...' not in x:
                try: valores_numericos.append(float(x))
                except ValueError: pass
                
    return eje_tiempo, valores_numericos


def home(request):
    error_msg = None

    if request.method == "POST" and request.FILES.getlist('file'):
        files = request.FILES.getlist('file')
        
        asegurar_imagen_base()
        
        id_unico = uuid.uuid4().hex[:8]
        container_name = f"contenedor_{id_unico}"
        datos_inicio_extraidos = {}
        
        try:
            # Analizamos el archivo .py para extraer variables con sus nombres reales
            for f in files:
                if f.name.endswith('.py'):
                    codigo_del_script = f.read().decode('utf-8')
                    datos_inicio_extraidos = extraer_variables_del_script(codigo_del_script)
                    f.seek(0)
            
            # Arrancar contenedor temporal
            subprocess.run([
                "docker", "run", "-d", 
                "--name", container_name, 
                "dockerfile", 
                "sh", "-c", "mkdir -p /app && tail -f /dev/null"
            ], check=True)
            
            # Copiar archivos
            for f in files:
                contenido_archivo = f.read()
                subprocess.run([
                    "docker", "exec", "-i", 
                    container_name, 
                    "sh", "-c", f"cat > /app/{f.name}"
                ], input=contenido_archivo, check=True)
            
            # Buscar el script de simulación
            script_a_ejecutar = next((f.name for f in files if f.name.endswith('.py')), None)
            
            if script_a_ejecutar:
                # 🔥 EL TRUCO MAESTRO: Ejecutamos un comando en línea que configura 
                # np.set_printoptions a infinito antes de leer y ejecutar tu archivo original.
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
                    # Extraemos el tiempo y la lista plana de concentraciones
                    t_lista, c_valores = limpiar_consola_numpy(salida_consola)
                    
                    # 🔥 FUSIONAMOS TODO EN EL JSON UNIFICADO GLOBAL (Soporta 1D, 2D y 3D plano)
                    json_unificado = {
                        "datos_inicio": datos_inicio_extraidos,  
                        "resultados_finales": {
                            "eje_tiempo": t_lista,
                            "valores_c_plano": c_valores  # Lista de valores pura e indestructible
                        }
                    }
                    
                    # Guardamos en la sesión
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

    return render(request, 'simulator/home.html', {'error': error_msg})

def simulator(request):
    # Sacamos el paquete de la sesión
    datos_sesion = request.session.get('simulacion_completa', None)
    
    # Lo transformamos en texto JSON limpio
    datos_json_string = json.dumps(datos_sesion) if datos_sesion else None

    # Se lo enviamos al HTML con el nombre 'json_simulacion'
    return render(request, 'simulator/simulator.html', {
        'json_simulacion': datos_json_string
    })
def data_definition(request):
    return render(request, 'simulator/data_definition.html', {})

def temporal_history(request):
    return render(request, 'simulator/temporal_history.html', {})