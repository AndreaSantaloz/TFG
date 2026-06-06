from django.core.files.storage import FileSystemStorage
import os
import numpy as np
from django.conf import settings
import random
from django.core.mail import send_mail
import subprocess
from django.contrib.auth.models import User
from .forms import sign_up_user_form,login_user_form,recover
import joblib
from django.contrib.auth.models import User
import subprocess
import sys
import ast
import os
import time
import shutil
from pathlib import Path
import datetime


"""
Aqui es la parte de ejecución
"""



def access_nav(id_user,name):
    return f"{settings.MEDIA_URL}/simulator/user_{id_user}/{name}"

def access_disk(id_user,name):
    return f"{settings.MEDIA_ROOT}/simulator/user_{id_user}/{name}"
    
def store_files(disk_position,base_url,file):
    fs = FileSystemStorage(location= disk_position, base_url=base_url)
    return fs.path(fs.save(file.name,file))


#Se cambiaran por DOCKER
def create_virtual_env(id_user):
    path = os.path.join(settings.MEDIA_ROOT,"simulator",f"user_{id_user}","enviorment")  
    print(path)
    os.makedirs(path,exist_ok=True)
    subprocess.run([sys.executable,'-m','venv',path],
                    capture_output=True, text=True, shell=True,check=True)
    #Cambiar segun sistema operativo(De momento hasta que sepa comprobar las librerias se ponen unas determinadas)

    instalator = os.path.join(path,'Scripts','pip.exe')
    subprocess.run([(instalator),'install']
                    +['numpy','matplotlib','scipy','pandas','scikit-learn','seaborn','polars','pillow'],
                    capture_output=True, text=True, shell=True,check=True)
    #comando para verificar la librerias subprocess.run([pip_executable, "list"], capture_output=True, text=True
    return path
    

def execute_model_user(enviorment,main):
    #Cojer un comando que encuentre el camino de donde estan los ficheros y ejecutar el main.py
    python_env = os.path.join(enviorment, "Scripts", "python.exe")
    print("Ejecutandose ...")
    r=subprocess.run([python_env,main], capture_output=True, text=True)
    return r.stdout
    


def stop_execute_model(user,base,time):
    if os.path.exists(base):
        print(f"the {user}  began at {time[0]} and finalished at {time[1]}.The {user} duro {time[2]}")
        #shutil.rmtree(base)
    else:
        print("El usuario no ha generado un entorno virtual")
    

def send_email_user(request):
    if request.method == "POST":
        form = recover(request.POST)
        if form.is_valid():
            email_input = form.cleaned_data['email']
            user_obj = User.objects.filter(email=email_input).first()
            if user_obj is not None:
                code=str(random.randint(100000,999999))
                request.session['recovery_code'] = code
                request.session['recovery_email'] = user_obj.email
                send_mail(
                    subject="Correo de prueba",
                    message="Tu código es : "+ str(code),
                    from_email = settings.EMAIL_HOST_USER,
                    recipient_list=[user_obj.email],
                    fail_silently=False,
                )





