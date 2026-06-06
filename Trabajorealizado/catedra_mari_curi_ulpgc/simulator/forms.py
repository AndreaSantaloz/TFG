from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import ProfileUser,UserModel
from django.contrib.auth import logout,authenticate, login as auth_login
class sign_up_user_form(forms.Form):
    areas_neurocience=[
            ("developmental_neurocience","Developmental neuroscience"),
            ("cognitive_neuroscience","Cognitive neuroscience"),
            ("molecular_and_cellular_neuroscience","Molecular and cellular neuroscience"),
            ("neurogenetics","Neurogenetics"),
            ("behavioral_neuroscience","Behavioral neuroscience"),
            ("clinicial_neuroscience","Clinical neuroscience"),
            ("neurophysiology","Neurophysiology"),
            ("sensory_neuroscience","Sensory neuroscience")         
        ]
    name=forms.CharField()
    email = forms.EmailField()
    institution = forms.CharField(max_length=19)
    orcid=forms.CharField()
    areas_of_specialization=forms.ChoiceField(
            choices=areas_neurocience,
            label="areas_neuroscience",
            widget=forms.Select(attrs={'id':'inputs'})
        )
    password= forms.CharField(widget=forms.PasswordInput)
    confirm_password= forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data =super().clean()
        password=cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError("Las contraseñas no coinciden")
    
    def create_user(self):
        return User.objects.create_user(
            username=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
    
    #Separar responsabilidad incumple SRP
    def create_profile_user(self,user):
        return ProfileUser.objects.create(
            user=user,
            institution = self.cleaned_data['institution'],
            orcid=self.cleaned_data['orcid'],
            areas_of_specialization=self.cleaned_data['areas_of_specialization'],
            image=None,
            abstract_personal=None,
            github=None,
        )


class login_user_form(forms.Form):
    
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email= cleaned_data.get('email')
        password=cleaned_data.get('password')
        user = User.objects.filter(email=email).first()
        if user:
            if authenticate(username=user.username,password=password):
                self.user_cache = user
            else:
                raise forms.ValidationError("La contraseña es incorrecta")
        else:
            raise forms.ValidationError("No existe el usuario")

        

class profile_user_form(forms.ModelForm):
    class Meta:
        model=ProfileUser
        fields=['image','abstract_personal']
    

class recover(forms.Form):
    email = forms.EmailField()

class add_model_form(forms.ModelForm):
    pass

class delete_model_form(forms.Form):
    pass


