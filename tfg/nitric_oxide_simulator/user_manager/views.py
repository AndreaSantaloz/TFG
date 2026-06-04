from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login ,logout

from django.contrib.auth.models import User
from .form import LoginForm
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user_sentence = User.objects.get(email=form.cleaned_data['email'])
            user = authenticate(request, 
                                username= user_sentence.username, 
                                password=form.cleaned_data['password']
                                )
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                pass
                #redirect('error')
    else:
        form = LoginForm()
    
    return render(request,'user_manager/login.html',{})

def sign_up_view(request):
    return render(request,'user_manager/sign_up_basic.html',{})

def sign_up_academic_view(request):
    return render(request,'user_manager/sign_up_academic.html',{})

def delete_acount_view(request):
     return render(request,'user_manager/application.html',{'title':'DELETE ACCOUNT','action':'deleting your account'})

def recover_password_view(request):
    return render(request,'user_manager/application.html',{'title':'RECOVER PASSWORD','action':'recovering your password'})

def change_password_view(request):
     return render(request,'user_manager/application.html',{'title':'CHANGE PASSWORD','action':'changing your password'})

def logout_view(request):
    logout(request)
    return redirect('index')