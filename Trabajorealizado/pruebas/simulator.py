import subprocess
import sys
import ast
import os
import time
import shutil
from pathlib import Path
import datetime
"""
Se tendra que adaptar a Path para los distintos sistemas operativos
"""

"""
En el entorno web habrá que quitar OS,Shutil,exec,eval,subprocess,path,fs
"""




def create_directory_temporal_simulator_for_user(user):
    os.makedirs(os.path.abspath(f'.simulator/{user}/'), exist_ok=True)
    os.makedirs(os.path.abspath(f'.simulator/{user}/files'), exist_ok=True)
    os.makedirs(os.path.abspath(f'.simulator/{user}/enviorment'), exist_ok=True)
    


def store_files_simulator(user,main,model):
    shutil.move(main, os.path.join(os.path.abspath(f'.simulator/{user}/files'), os.path.basename(main)))
    shutil.move(model, os.path.join(os.path.abspath(f'.simulator/{user}/files'),  os.path.basename(model)))



def create_virtual_env(user):
    subprocess.run([sys.executable,'-m','venv', os.path.abspath(f'.simulator/{user}/enviorment')],
                    capture_output=True, text=True, shell=True,check=True)
    #Cambiar segun sistema operativo(De momento hasta que sepa comprobar las librerias se ponen unas determinadas)
    subprocess.run([ os.path.join(os.path.abspath(f'.simulator/{user}/enviorment'), 'Scripts', 'pip.exe'),'install']
                    +['numpy','matplotlib','scipy','pandas','scikit-learn','seaborn','polars','pillow'],
                    capture_output=True, text=True, shell=True,check=True)
    #comando para verificar la librerias subprocess.run([pip_executable, "list"], capture_output=True, text=True
    return os.path.abspath(f'.simulator/{user}/enviorment')
    

def execute_model_user(enviorment,main):
    #Cojer un comando que encuentre el camino de donde estan los ficheros y ejecutar el main.py
    tiempo_inicial=time.time()
    first_date=datetime.datetime.now()
    python_env = os.path.join(enviorment, "Scripts", "python.exe")
    result = subprocess.run([python_env,main], capture_output=True, text=True)
    tiempo_final=time.time()
    last_date = datetime.datetime.now()
    tiempo = tiempo_final - tiempo_inicial
    return [first_date,last_date,tiempo]
    
def stop_execute_model(user,base,time):
    if os.path.exists(base):
        print(f"the {user}  began at {time[0]} and finalished at {time[1]}.The {user} duro {time[2]}")
        #shutil.rmtree(base)
    else:
        print("El usuario no ha generado un entorno virtual")
    
if __name__=="__main__":
    user="user2"
    model=os.path.abspath(f'.users/{user}/prueba.py')
    main=os.path.abspath(f'.users/{user}/main.py')
    create_directory_temporal_simulator_for_user("user2")
    store_files_simulator(user,main,model)
    enviorment = create_virtual_env(user)
    main= f'.simulator/{user}/files/main.py'
    time_and_date_execution = execute_model_user(enviorment,main)
    base= os.path.abspath(f'.simulator/{user}/')
    stop_execute_model(user,base,time_and_date_execution)