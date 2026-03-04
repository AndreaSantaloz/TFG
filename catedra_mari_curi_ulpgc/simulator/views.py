from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .forms import sign_up_user_form,login_user_form
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User

def index(request):
    template = loader.get_template("simulator/index.html")
    return HttpResponse(template.render({},request))

def login(request):
    if request.method == "POST":
        form = login_user_form(request.POST)
        if form.is_valid():
            email_input = form.cleaned_data['email']
            password_input = form.cleaned_data['password']
            user_obj = User.objects.filter(email=email_input).first()
            if user_obj is not None:
                user = authenticate(request, username=user_obj.username, password=password_input)
                if user is not None:
                    auth_login(request, user)
                    return redirect('simulator')
                else:
                    messages.error(request, "Contraseña incorrecta.")
            else:
                messages.error(request, "Este correo electrónico no está registrado.")
        else:
            messages.error(request, "Por favor, rellena los campos correctamente.")
    else:
        form = login_user_form()
        
    return render(request, "simulator/login.html", {'form': form})

def sign_up(request):
    if request.method == "POST":
        form = sign_up_user_form(request.POST)
        if form.is_valid():
            form.create_user()
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = sign_up_user_form()

    return render(request,"simulator/sign_up.html",{'form':form})


def simulator(request):
    return render(request,"simulator/simulator.html",{})
    
def profile(request):
    return HttpResponse("En mantenimiento")

    
def store(request):
    return HttpResponse("En mantenimiento")

    
def setting(request):
    return HttpResponse("En mantenimiento")

    
def upload_model(request):
    return HttpResponse("En mantenimiento")


def tabular_chart(request):
    return render(request,"simulator/table.html",{})
    
def dispersion_chart(request):
    return render(request,"simulator/dispersion_charts.html",{})
    
def correlation_chart(request):
    return render(request,"simulator/correlation_charts.html",{})
    
    
def volume_chart(request):
    return render(request,"simulator/volume_charts.html",{})
    
def errors_chart(request):
        return render(request,"simulator/errors_charts.html",{})

    
