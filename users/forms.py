from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Button
from crispy_forms.bootstrap import InlineField

from phonenumber_field.formfields import PhoneNumberField


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        
class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True, label = 'Votre mail')
    subject = forms.CharField(required=True, label = 'Sujet')
    message = forms.CharField(widget=forms.Textarea, required=True)
    
class SignupForm(forms.Form):
    email = forms.EmailField(required=True, label = 'Votre mail',widget=forms.TextInput(attrs={'class': 'form-control'}))
    nom = forms.CharField(max_length=25, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    prenom = forms.CharField(max_length=25, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    adresse1 = forms.CharField(max_length=40, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    adresse2 = forms.CharField(max_length=40, required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    codepostal = forms.IntegerField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    ville = forms.CharField(max_length=35, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    telephone = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': _('N° avec indicatif Pays - ex 0612345678 devient +33612345678. En france, on remplace le 1er zéro par +33'),'class': 'form-control'}),label=_("Phone number"), required=True)
    telephone.error_messages={'invalid': 'N° avec indicatif Pays - ex 0612345678 devient +33612345678. En france, on remplace le 1er zéro par +33'}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nom', css_class='form-group col-lg-6 col-md-6 mb-0'),
                Column('prenom', css_class='form-group col-lg-6 col-md-6 mb-0'),

            ),
            'email',
            'telephone',
            'adresse1',
            'adresse2',
            Row(
                Column('codepostal', css_class='form-group col-md-3 mb-0'),
                Column('ville', css_class='form-group col-md-9 mb-0'),
            ),
             HTML("<br>"), 
             Row(
                Button('cancel', 'Annuler',css_class='form-group col-md-4 mb-0 btn-info'),
                Submit('submit', 'Soumettre',css_class='form-group col-md-4 mb-0 btn-danger'),
                css_class='form-row'
            ),

        )


class Okpourcontinuer(forms.Form):
    pass

class LoginForm(forms.Form):
    """user login form"""
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
