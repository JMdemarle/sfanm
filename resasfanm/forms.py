from django import forms
from .models import Reservation, Capacite, Presence

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from crispy_forms.bootstrap import InlineField

from datetime import date, datetime
#from bootstrap_datepicker_plus import DatePickerInput

#from bootstrap_modal_forms.forms import BSModalForm


class NewReservationForm(forms.Form):
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_arguments = kwargs.get('initial', None)

        self.datedepot = initial_arguments.get('la_date',None)
        self.datechoix = initial_arguments.get('choix_date',None)
        
#        self.fields['api'] = forms.CharField(max_length=25)
        self.fields['nbreine'] = forms.IntegerField(label = 'Nombre reines', required = True)
        self.fields['datedepot'] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'},format=('%Y-%m-%d')),initial=self.datedepot, disabled = True)
#        self.fields['dateretrait'] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'},format=('%Y-%m-%d')))
        self.fields['dateretrait'] = forms.ChoiceField(choices = self.datechoix) 

        self.fields['nbtypfecond1'] = forms.IntegerField(label = 'Nombre Apidéa/Kieler  ', required = True)
        self.fields['nbtypfecond2'] = forms.IntegerField(label = 'Nombre MiniPlus       ', required = True)
        self.fields['nbtypfecond3'] = forms.IntegerField(label = 'Nombre Warré          ', required = True)
        self.fields['nbtypfecond4'] = forms.IntegerField(label = 'Nombre Ruchette-dadant', required = True)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'nbreine',
            Row(
                Column('datedepot', css_class='form-group col-md-3 mb-0'),
                Column('dateretrait', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('nbtypfecond1', css_class='form-group col-md-3 mb-0'),
                Column('nbtypfecond2', css_class='form-group col-md-3 mb-0'),
                Column('nbtypfecond3', css_class='form-group col-md-3 mb-0'),
                Column('nbtypfecond4', css_class='form-group col-md-3 mb-0'),
            ),
            HTML("<br>"),
            Submit('submit', 'Créer')
        )

class ModReservationForm(forms.Form):

    nbreine = forms.IntegerField(label = 'Nombre reines', required = True)
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_arguments = kwargs.get('initial', None)

        self.datedepot = initial_arguments.get('la_date',None)
        self.datechoix = initial_arguments.get('choix_date',None)
        self.resa = initial_arguments.get('la_resa',None)
        
        #self.fields['nbreine'] = forms.IntegerField(label = 'Nombre reines', required = True, initial = self.resa.nbreine)
        self.fields['datedepot'] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'},format=('%Y-%m-%d')),initial=self.datedepot, disabled = True)
        self.fields['dateretrait'] = forms.ChoiceField(choices = self.datechoix) 

        self.fields['nbtypfecond1'] = forms.IntegerField(label = 'Nombre Apidéa/Kieler  ', required = True)
        self.fields['nbtypfecond2'] = forms.IntegerField(label = 'Nombre MiniPlus       ', required = True)
        self.fields['nbtypfecond3'] = forms.IntegerField(label = 'Nombre Warré          ', required = True)
        self.fields['nbtypfecond4'] = forms.IntegerField(label = 'Nombre Ruchette-dadant', required = True)

        self.fields["nbreine"].initial = self.resa.nbreine
        self.fields['datedepot'].initial = self.resa.datedepot
        self.fields['dateretrait'].initial = self.resa.dateretrait
        self.fields['nbtypfecond1'].initial = self.resa.nbtypfecond1
        self.fields['nbtypfecond2'].initial = self.resa.nbtypfecond2
        self.fields['nbtypfecond3'].initial = self.resa.nbtypfecond3
        self.fields['nbtypfecond4'].initial = self.resa.nbtypfecond4
        
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'nbreine',
            Row(
                Column('datedepot', css_class='form-group col-md-3 mb-0'),
                Column('dateretrait', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('nbtypfecond1', css_class='form-group col-md-3 mb-0'),
                Column('nbtypfecond2', css_class='form-group col-md-3 mb-0'),
                Column('nbtypfecond3', css_class='form-group col-md-3 mb-0'),
                Column('nbtypfecond4', css_class='form-group col-md-3 mb-0'),
            ),
            HTML("<br>"),
            Submit('submit', 'Modifier')
        )

 
