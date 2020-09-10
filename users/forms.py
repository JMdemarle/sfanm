from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Button, Div
from crispy_forms.bootstrap import InlineField



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
    telephone = forms.CharField(max_length=15, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
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
                Submit('submit', 'Soumettre',css_class='form-group col-lg-3 col-md-4 mb-0 btn-danger'),
                css_class='form-row'
            ),

        )


class ModMembreForm(forms.Form):
    is_active = forms.BooleanField(required=False, label ='actif')
    acquitte = forms.BooleanField(required=False, label ='reçu envoyé')
    nbreinesmax = forms.IntegerField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_arguments = kwargs.get('initial', None)
        self.le_membre = initial_arguments.get('le_membre',None)
        
        self.fields['is_active'].initial = self.le_membre.is_active
        self.fields['acquitte'].initial = self.le_membre.acquitte
        self.fields['nbreinesmax'].initial = self.le_membre.nbreinesmax
        
  
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('is_active', css_class='form-group col-lg-4 col-md-4 mb-0'),
                Column('acquitte', css_class='form-group col-lg-4 col-md-4 mb-0'),
                Column('nbreinesmax', css_class='form-group col-lg-4 col-md-4 mb-0'),

            ),
             HTML("<br>"), 
             Row(
                Submit('cancel', 'Annuler',css_class='form-group col-md-4 mb-0 btn-info',formnovalidate='formnovalidate',),
                Submit('submit', 'Soumettre',css_class='form-group col-md-4 mb-0 btn-danger'),
                css_class='form-row'
            ),
        )


class MonCompteForm(forms.Form):
    nom = forms.CharField(max_length=25, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    prenom = forms.CharField(max_length=25, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    adresse1 = forms.CharField(max_length=40, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    adresse2 = forms.CharField(max_length=40, required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    codepostal = forms.IntegerField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    ville = forms.CharField(max_length=35, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    telephone = forms.CharField(max_length=15, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_arguments = kwargs.get('initial', None)
        self.le_user = initial_arguments.get('le_user',None)
        
        self.fields['nom'].initial = self.le_user.nom
        self.fields['prenom'].initial = self.le_user.prenom
        self.fields['adresse1'].initial = self.le_user.adresse1
        self.fields['adresse2'].initial = self.le_user.adresse2
        self.fields['codepostal'].initial = self.le_user.codepostal
        self.fields['ville'].initial = self.le_user.ville
        self.fields['telephone'].initial = self.le_user.telephone
        
  
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nom', css_class='form-group col-lg-6 col-md-6 mb-0'),
                Column('prenom', css_class='form-group col-lg-6 col-md-6 mb-0'),

            ),
            'telephone',
            'adresse1',
            'adresse2',
            Row(
                Column('codepostal', css_class='form-group col-md-3 mb-0'),
                Column('ville', css_class='form-group col-md-9 mb-0'),
            ),
             HTML("<br>"), 
             Row(
                Submit('cancel', 'Annuler',css_class='form-group col-md-4 mb-0 btn-info',formnovalidate='formnovalidate',),
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
  
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div (
                'email',
                'password',
                HTML("<br>"), 
            
                Submit('submit', "S'identifier",css_class='form-group col-md-4 mb-0 btn-primary btn-block'),
                css_class="mw-100",
 
            )
        )
    
