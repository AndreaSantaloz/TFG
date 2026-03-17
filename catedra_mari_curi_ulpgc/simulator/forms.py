from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class sign_up_user_form(forms.Form):
    name = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")      
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Las contraseñas no coinciden")
        if password and len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres")
        return cleaned_data

    def create_user(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']    
        password = self.cleaned_data['password']
        return User.objects.create_user(username=name,email=email,password=password)



class login_user_form(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

"""
class upload_correct_files(forms.Form):
    file1=forms.FileField()
    file2=forms.FileField()
    if file1.size < 500000 and file2 < 500000:
        pass
    class Meta:
        pass
    pass
    
    """