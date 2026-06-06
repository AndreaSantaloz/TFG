import subprocess
import sys
import ast
import os

#Aqui tengo que establecer la ruta del amin
# Cada vez que se crea un usuario se genera una carpeta del usuario con las siguientes herramientas
"""
user + id
-media
    -simulator
        Opcion A
        -simulations asociadas al id del usuario
        -enviorments asociados al ide del usuario
        -ficheros para la simulacion asociados al id del usuario
        
        ------------------------
        |id|id user|enviorment|ficheros|first_access|last_access|(Simulation 1)
        |id|id user|enviorment|ficheros|first_access|last_access|(Simulation 2)
        |id|id user|enviorment|ficheros|first_access|last_access|(Simulation 3)
        |id|id user|enviorment|ficheros|first_access|last_access|(Simulation 4)

        Un enviorment como lo desglosamos
        Tiene include
        Tiene Lib
        Tiene Scripts
        Tiene share
        Tiene pyvenv.cfg

        Opcion B    
        -use + id
            -simulations + id (registro de simulaciones)()
            -simulator_enviorment asociada a la simulacion Tras finalizar la simulacion se elimina(Temporal)
            -simulator_files asociada a la simulacion Tras finalizar la simulacion se elimina(Temporal)
                -main
                -modelo
        -use + id
            -simulations + id (registro de simulaciones)
            -simulator_enviorment asociada a la simulacion Tras finalizar la simulacion se elimina(Temporal)
            -simulator_files asociada a la simulacion Tras finalizar la simulacion se elimina(Temporal)
                -main
                -modelo
        -use N
    -images
        -user+id + profile
            -image
            
    -users
        -user-id(el nombre de un modelo no puede ser main)
            -model
            -model
            
-
"""

"""
Crear entorno virtual para usuario 
:param: usuario
:return: camino creado
sim
symbolb
"""
def create_virtual_env(user):
    enviorment_path =  os.path.abspath(f'.users/{user}/simulator_enviorment/enviorment')
    pip_executable = os.path.join(enviorment_path, 'Scripts', 'pip.exe') #Cambiar a linux cuando se pase al servidor
    # Establecer tiempo
    subprocess.run([sys.executable,'-m', 'venv', enviorment_path],capture_output=True, text=True, shell=True,check=True)
    #Cambiar segun sistema operativo(De momento hasta que sepa comprobar las librerias se ponen unas determinadas)
    subprocess.run([pip_executable,'install','numpy'],capture_output=True, text=True, shell=True,check=True)
    subprocess.run([pip_executable,'install','matplotlib'],capture_output=True, text=True, shell=True,check=True)
    subprocess.run([pip_executable,'install','scipy'],capture_output=True, text=True, shell=True,check=True)
    subprocess.run([pip_executable,'install','pandas'],capture_output=True, text=True, shell=True,check=True)
    subprocess.run([pip_executable,'install','sckit-learn'],capture_output=True, text=True, shell=True,check=True)
    subprocess.run([pip_executable,'install','seaborn'],capture_output=True, text=True, shell=True,check=True)
    #comando para verificar la librerias subprocess.run([pip_executable, "list"], capture_output=True, text=True)
    return enviorment_path


"""
Ejecutar modelo 
:param: enviorment creado
:return: valores calculados del modelo
"""
def execute_model_user(enviorment,ficheros_path):
    #Cojer un comando que encuentre el camino de donde estan los ficheros y ejecutar el main.py
    subprocess.run([enviorment, sys.executable,'main.py'], capture_output=True, text=True)
"""
Crear gráficas 
:param: resultados del modelo
:return: graficas
"""
def create_charts(results):
    pass
"""
Revisar fichero de modelo y main.py
:param: usuario
:param: enviorment creado
:return: comprobado ficheros sin un good sino si no hay error sigue la ejecucion
"""
def revise_code(user):
    #Aqui en 
    user_path=""
    try:
        with open(f'.simulator/{user}/simulator_files/{user_path}','r') as code:
        #Revisar el codigo   
            code = code.read()
            tree = ast.parse(code)
            instance_import=[]
            instance_from_import = []
            for nodo in ast.walk(tree):
                if isinstance(nodo,ast.Import):
                    instance_import+=[n.name for n in nodo.names]
                elif isinstance(nodo,ast.ImportFrom):
                    instance_from_import.append(nodo.module)
            print(f"Import: {instance_import}")
            print(f"Import from: {instance_from_import}")
            
            if len(instance_from_import) == 0:
                return "Finish the revision"
            else:
                for imports in instance_from_import:
                    revise_code(imports)
                    
    except OSError as err:
        print("Error del sistema: " + err)
    except NameError:
        print("La variable main_code no se esta generando al no existir el fichero ")
    except FileExistsError:
        print("El fichero ya existe ")
    except FileNotFoundError:
        print("El fichero no se encuentra")
    except Exception as e:
        print("Error inesperado")
    

if __name__=="__main__":
    usuario=".users/user1"
    if os.path.exists(usuario):
        print("Existe")
        print("Su contenido es :")
        print(os.listdir('.users/user1'))
    else:
        print("No existe")
