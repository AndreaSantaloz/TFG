
import os
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .forms import sign_up_user_form,login_user_form,recover,profile_user_form,add_model_form
from .utils import access_nav,access_disk,store_files,send_email_user,create_virtual_env,execute_model_user
from .models import ProfileUser, UserModel
from urllib.parse import urlencode
from django.contrib.auth import logout,login 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
import subprocess
import numpy as np
import ast
import json
import re
def index(request):
    return render(request,"index.html",{})

def login_view(request):
    if request.method == "POST":
        form = login_user_form(request.POST)
        if form.is_valid():
            login(request,form.user_cache)
            return redirect('home')
        else:
            return render(request, "authentication/login.html", {'form':form})
    else:
         form = login_user_form()
    

    return render(request, "authentication/login.html", {})

def sign_up(request):
    if request.method == "POST":
            form = sign_up_user_form(request.POST)
            if form.is_valid():
                messages.success(request,"Usuario registrado con éxito")
                if form.create_user() is not None:
                    form.create_profile_user(form.create_user())
                    return redirect('login')
            else:
                messages.error(request,"Formulario inválido")
            return render(request,"authentication/sign_up.html",{'form':form})
    else:
        form = sign_up_user_form()
        messages.error(request,"Error en la solicitud")
    return render(request,"authentication/sign_up.html",{})



def about_this_app(request):
    return render(request,"index-pages/about_this_app.html",{})
def help(request):
    return render(request,"index-pages/help.html",{})
def privacy_terms(request):
    return render(request,"index-pages/privacy_terms.html",{})


#Subida de ficheros
@login_required
def home(request):
    if request.method == 'POST' and request.FILES['input_file'] and request.FILES['model']:
            input_file=store_files(
                access_disk(request.user.id,'files'),
                access_nav(request.user.id,'files'),
                request.FILES['input_file'],
            )
            model = store_files(
                access_disk(request.user.id,'files'),
                access_nav(request.user.id,'files'),
                request.FILES['model'],
            )
            
            request.session["input_data"] =input_file
            request.session["model"] = model
            return redirect('checking_inputs')
            
    return render(request,'simulator_process/home.html',{})

"""
1. Aqui se comprobara el modelo y el main.py para ver si estan corruptos
2. Se redigira al simulador 
"""
@login_required
def checking_inputs(request):
    input_data= request.session.get("input_data")
    model = request.session.get("model")
    id=request.user.id
    user = User.objects.get(id=request.user.id)
    path_env= create_virtual_env(id)
    result = execute_model_user(path_env,input_data)
    print(result)
    print("Fin de la ejecución resultado")
    # Se va a cambiar todo este apartado
    matches = re.findall(r'\[.*?\]', result, re.DOTALL)
    extracted_lists = []
    for m in matches:
        clean_numbers = re.sub(r'[\[\]\n]', '', m).replace(',', ' ').split()
        extracted_lists.append([float(x) for x in clean_numbers])
    if len(extracted_lists) >= 2:
        transform_arrays = (np.array(extracted_lists[0]), np.array(extracted_lists[1:]))
    else:
        transform_arrays = tuple(np.array(x) for x in extracted_lists)
    # De momento asi hasta que sepa como contextualizar
    print(transform_arrays[0].tolist())
    print(transform_arrays[1].tolist())
    request.session["time"]=transform_arrays[0].tolist()
    request.session["concentration"]=transform_arrays[1].tolist()
    return render(request,'simulator_process/checking_inputs.html',{})
    
@login_required
def simulator(request):
    return render(request,'simulator_process/simulator.html',{"time":(request.session.get("time")),
                                                              "concentration":( request.session.get("concentration"))
                                                              })


#Cambiar perfil
@login_required  
def profile(request):
    return render(request,"profile/profile.html",  { 'name':(User.objects.get(id=request.user.id)).username,
                                                     'email':((User.objects.get(id=request.user.id)).email),
                                                     'institution':(ProfileUser.objects.get(user=(User.objects.get(id=request.user.id)))).institution,
                                                     'areas_of_specialization':((ProfileUser.objects.get(user=(User.objects.get(id=request.user.id)))).areas_of_specialization),
                                                     'abstract_personal': ((ProfileUser.objects.get(user=(User.objects.get(id=request.user.id)))).abstract_personal),
                                                     'image':((ProfileUser.objects.get(user=(User.objects.get(id=request.user.id)))).image),      
                                                    })


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = profile_user_form(request.POST,request.FILES,instance=(ProfileUser.objects.get(user=request.user.id)))
        return  form.save(),redirect('profile')  if form.is_valid() else messages.error(request,"Formulario no válido")
    else:
        form = profile_user_form(instance=(ProfileUser.objects.get(user=request.user.id)))
        messages.error(request,"Error en la solicitud")

    return render(request,"setting/edit_profile.html",{'form':form,
                                                       'name':(User.objects.get(id=request.user.id)).username,
                                                       'email':((User.objects.get(id=request.user.id)).email),
                                                       'institution':(ProfileUser.objects.get(user=(User.objects.get(id=request.user.id)))).institution,
                                                       })

"""
ALMACENAMIENTO
"""

# Full path para comprobar que esta en el disco(Cambiar)
@login_required 
def store(request):
    user = access_disk(request.user.id,'models')
    lista_modelos = []
    if os.path.exists(user):
        for nombre_archivo in os.listdir(user):
            url_archivo = os.path.join(access_nav(request.user.id,'models'), nombre_archivo)
            nombre_base, extension = os.path.splitext(nombre_archivo)
    
            lista_modelos.append({
                'nombre': nombre_archivo,
                'url': os.path.join(access_nav(request.user.id,'models'), nombre_archivo),
                'formato': extension 
            })

        
        return render(request,"others/store.html",{'modelos': lista_modelos})
    else:
        return render(request,"others/store.html",{})


#Pop up de almacenamiento(cambiar)
@login_required
def add_model(request):
    if request.method == "POST" and request.FILES['model'] :
        store_files(
                access_disk(request.user.id,'models'),
                access_nav(request.user.id,'models'),
                request.FILES['model'],
            )

    return render(request, 'popups/add_model.html', {})

@login_required
def  delete_model(request):
    return render(request,'popups/delete_model.html',{})



"""
AJUSTES DE USUARIO
"""

@login_required
def setting(request):
    return render(request,"setting/setting.html",{})



def recover_password(request):
    send_email_user(request)
    return render(request,"setting/recover_password.html",{})



@login_required
def change_password(request):
    send_email_user(request)
    return render(request,"setting/change_password.html",{})

@login_required
def delete_account(request):
    send_email_user(request)
    return render(request,"setting/delete_account.html",{})


@login_required
def tutorial(request):
    return render(request,"others/tutorial.html",{})


"""
Acciones de usuario
"""
@login_required
def exit(request):
    logout(request)
    return redirect('index')