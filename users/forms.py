from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        
class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True, label = 'Votre mail')
    subject = forms.CharField(required=True, label = 'Sujet')
    message = forms.CharField(widget=forms.Textarea, required=True)
    

class Okpourcontinuer(forms.Form):
    pass

class LoginForm(forms.Form):
    """user login form"""
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
