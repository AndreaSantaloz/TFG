from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User
from .form import LoginForm,SignUpFirstStepForm,SignUpSecondStepForm
from .models import Profile_User
from django.contrib import messages
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user_sentence = User.objects.get(email=form.cleaned_data['email'])
                user = authenticate(request, 
                                username= user_sentence.username, 
                                password=form.cleaned_data['password']
                                )
            
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, "The user does not exist")
            except User.DoesNotExist:
                messages.error(request, "The user does not exist")
        else:
              messages.error(request, "Falta un campo")

    else:
        form = LoginForm()
    
    return render(request,'user_manager/login.html',{})

def sign_up_view(request):
    if request.method == "POST":
        form = SignUpFirstStepForm(request.POST)
        if form.is_valid():
            print("Funcionas")
            request.session["data_user"]={
                'name':form.cleaned_data['name'],
                'email':form.cleaned_data['email'],
                'password':form.cleaned_data['password'],
            }
            return redirect('sign_up_academic')
        else:
            print("No funciona")
            pass
    else:
        print("No entra al formulario")
        form = SignUpFirstStepForm()

    return render(request,'user_manager/sign_up_basic.html',{'form':form})

def sign_up_academic_view(request):
    if request.method == "POST":
        form = SignUpSecondStepForm(request.POST)
        if form.is_valid():
            data = request.session.get('data_user')
            print(data)
            user = User.objects.create_user(data['name'],
                                     data['email'],
                                     data['password']
                                     )
            Profile_User.objects.create(user = user,
                                                        institution = form.cleaned_data['institution'],
                                                        researchfield = form.cleaned_data['researchfield'],
                                                        researcharea =  form.cleaned_data['researcharea'],
                                                       )
            return redirect('login')
        else:
            pass
    else:
        form = SignUpSecondStepForm()
    return render(request,'user_manager/sign_up_academic.html',{'form':form})

def delete_acount_view(request):
     return render(request,'user_manager/application.html',{'title':'DELETE ACCOUNT','action':'deleting your account'})

def recover_password_view(request):
    return render(request,'user_manager/application.html',{'title':'RECOVER PASSWORD','action':'recovering your password'})

def change_password_view(request):
     return render(request,'user_manager/application.html',{'title':'CHANGE PASSWORD','action':'changing your password'})


def user_profile(request):
    profile_user = Profile_User.objects.get(user=request.user)
    return render(request,'user_manager/user_profile.html',{'name':request.user.username,
                                                                    'email': request.user.email,
                                                                    'institution':profile_user.institution,
                                                                     'researchfield':profile_user.researchfield,
                                                                      'researcharea':profile_user.researcharea,
                                                                      'image':profile_user.image,
                                                                      'aboutuser':profile_user.aboutuser,
                                                                      'researchs':profile_user.researchs,
                                                                    })
def logout_view(request):
    logout(request)
    return redirect('index')


def settings(request):
    return render(request,'user_manager/settings.html',{})

def account_settings(request):
    return render(request,'user_manager/account_settings.html',{})
def accesibility_settings(request):
    return render(request,'user_manager/accesibility_settings.html',{})
def edit_profile(request):
    return render(request,'user_manager/edit_profile.html',{})