from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label="Password", 
                               widget=forms.PasswordInput,
                               min_length=8,
                               max_length=32,
                               )

