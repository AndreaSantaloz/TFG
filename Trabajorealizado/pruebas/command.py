"""
python -m venv .users/user2/venvs/simulator-env
"""


import subprocess
import sys
import venv
import os

env_path =  os.path.abspath('.users/user2/simulator/simulator-env')

# Establecer tiempo
virtual_env_user = subprocess.run([sys.executable,'-m', 'venv', env_path],capture_output=True, text=True, shell=True,check=True)
#Cambiar segun sistema operativo(De momento hasta que sepa comprobar las librerias se ponen unas determinadas)
pip_executable = os.path.join(env_path, 'Scripts', 'pip.exe')
install_numpy = subprocess.run([pip_executable,'install','numpy'],capture_output=True, text=True, shell=True,check=True)
install_matplotlib = subprocess.run([pip_executable,'install','matplotlib'],capture_output=True, text=True, shell=True,check=True)
install_scipy = subprocess.run([pip_executable,'install','scipy'],capture_output=True, text=True, shell=True,check=True)
verificacion = subprocess.run([pip_executable, "list"], capture_output=True, text=True)
print(verificacion.stdout) 
ejecucion = subprocess.run([env_path, sys.executable,'main.py'], capture_output=True, text=True)
env_path