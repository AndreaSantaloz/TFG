from django import forms
from django.core.exceptions import ValidationError
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label="password", 
                               widget=forms.PasswordInput,
                               min_length=8,
                               max_length=32,
                               )

class SignUpFirstStepForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(label="password", 
                               widget=forms.PasswordInput,
                               min_length=8,
                               max_length=32,
                               )
    confirm_password = forms.CharField(label="confirm_password", 
                               widget=forms.PasswordInput,
                               min_length=8,
                               max_length=32,
                               )
    def clean(self):
        cleaned = super().clean()
        password_one = cleaned.get('password')
        password_two = cleaned.get('confirm_password')
        if password_one != password_two:
            raise ValidationError(
                'Password incorrect'
            )
        return cleaned

  
   
class SignUpSecondStepForm(forms.Form):
    institution = forms.CharField()
    researchfield= forms.CharField()
    researcharea=forms.CharField()
   