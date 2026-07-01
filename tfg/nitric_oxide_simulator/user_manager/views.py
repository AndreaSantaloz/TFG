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



def user_profile(request):
    
    profile_user = Profile_User.objects.get(user=request.user)    
    display_name = request.user.first_name if request.user.first_name else request.user.username
    return render(request, 'user_manager/user_profile.html', {
        'name': display_name, 
        'email': request.user.email,
        'institution': profile_user.institution,
        'researchfield': profile_user.researchfield,
        'researcharea': profile_user.researcharea,
        'aboutme': profile_user.aboutuser,  
        'researchs': profile_user.researchs, 
    })
    
def logout_view(request):
    logout(request)
    return redirect('index')

def edit_profile(request):
    user = request.user
    profile, created = Profile_User.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        institution = request.POST.get('institution')
        researchfield = request.POST.get('researchfield')
        researcharea = request.POST.get('researcharea')
        aboutme = request.POST.get('aboutme') 
        researchs = request.POST.get('researchs')
        
        user.username = name
        user.save()
        
        profile.institution = institution
        profile.researchfield = researchfield
        profile.researcharea = researcharea
        profile.aboutuser = aboutme  
        profile.researchs = researchs
        profile.save()
        
        
        
        return redirect('user_profile') 
    context = {
        'name': user.username,
        'email': user.email,
        'institution': profile.institution,
        'researchfield': profile.researchfield,
        'researcharea': profile.researcharea,
        'aboutme': profile.aboutuser,
        'researchs': profile.researchs,
    }
    return render(request, 'user_manager/edit_profile.html', context)
    
