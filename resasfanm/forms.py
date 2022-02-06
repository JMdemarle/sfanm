from django import forms
from .models import Reservation, Capacite, Presence, Evenement, TypEmail

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, ButtonHolder
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
        self.fields['nbreine'] = forms.IntegerField(label = 'Nombre reines', required = True,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['datedepot'] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class': 'form-control'},format=('%Y-%m-%d')),initial=self.datedepot, disabled = True)
#        self.fields['dateretrait'] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'},format=('%Y-%m-%d')))
        self.fields['dateretrait'] = forms.ChoiceField(choices = self.datechoix,widget=forms.Select(attrs={'class': 'form-control'})) 

        self.fields['nbtypfecond1'] = forms.IntegerField(label = 'Nombre Apidéa/Kieler  ', required = True,initial='0',widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['nbtypfecond2'] = forms.IntegerField(label = 'Nombre MiniPlus       ', required = True,initial='0',widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['nbtypfecond3'] = forms.IntegerField(label = 'Nombre Warré          ', required = True,initial='0',widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['nbtypfecond4'] = forms.IntegerField(label = 'Nombre Ruchette-dadant', required = True,initial='0',widget=forms.TextInput(attrs={'class': 'form-control'}))
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nbreine', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('datedepot', css_class='form-group col-md-3 mb-0'),
                Column('dateretrait', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('nbtypfecond1', css_class='form-group col-lg-3 col-md-6 mb-0'),
                Column('nbtypfecond2', css_class='form-group col-lg-3 col-md-6 mb-0'),
                Column('nbtypfecond3', css_class='form-group col-lg-3 col-md-6 mb-0'),
                Column('nbtypfecond4', css_class='form-group col-lg-3 col-md-6 mb-0'),
            ),
            HTML("<br>"),
            Row(

                HTML("<div class='col-lg-3 col-sm-3'><a href='{% url 'capacites'  %}' class='btn btn-outline-success btn-block'>Revenir</a></div>"),
                HTML("<button type='submit' class='col-lg-3 col-sm-3 btn btn-outline-primary btn-block', >Réserver</button>"),
            ),
        )

class NewReservationApiForm(forms.Form):
     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_arguments = kwargs.get('initial', None)

        self.datedepot = initial_arguments.get('la_date',None)
        self.datechoix = initial_arguments.get('choix_date',None)
        self.lesApis = initial_arguments.get('les_apis',None)
#        self.strurlEntrees = "'listentrees'" + ' ' + "'" + self.datedepot.isoformat() + "'" 
        self.strurlEntrees = "'listgestion'" 


        self.fields['apiculteur'] = forms.ChoiceField(choices = self.lesApis,widget=forms.Select(attrs={'class': 'form-control'})) 
        self.fields['apiculteur'].choices = [(x.id, x.get_nom()) for x in self.lesApis]

#        self.fields['api'] = forms.CharField(max_length=25)
        self.fields['nbreine'] = forms.IntegerField(label = 'Nombre reines', required = True,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['datedepot'] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class': 'form-control'},format=('%Y-%m-%d')),initial=self.datedepot, disabled = True)
#        self.fields['dateretrait'] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'},format=('%Y-%m-%d')))
        self.fields['dateretrait'] = forms.ChoiceField(choices = self.datechoix,widget=forms.Select(attrs={'class': 'form-control'})) 

        self.fields['nbtypfecond1'] = forms.IntegerField(label = 'Nombre Apidéa/Kieler  ', required = True,initial='0',widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['nbtypfecond2'] = forms.IntegerField(label = 'Nombre MiniPlus       ', required = True,initial='0',widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['nbtypfecond3'] = forms.IntegerField(label = 'Nombre Warré          ', required = True,initial='0',widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['nbtypfecond4'] = forms.IntegerField(label = 'Nombre Ruchette-dadant', required = True,initial='0',widget=forms.TextInput(attrs={'class': 'form-control'}))
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row (Column('apiculteur', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('nbreine', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('datedepot', css_class='form-group col-md-3 mb-0'),
                Column('dateretrait', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('nbtypfecond1', css_class='form-group col-lg-3 col-md-6 mb-0'),
                Column('nbtypfecond2', css_class='form-group col-lg-3 col-md-6 mb-0'),
                Column('nbtypfecond3', css_class='form-group col-lg-3 col-md-6 mb-0'),
                Column('nbtypfecond4', css_class='form-group col-lg-3 col-md-6 mb-0'),
            ),
            HTML("<br>"),
            Row(

                HTML("<div class='col-lg-3 col-sm-3'><a href='{% url " + self.strurlEntrees + " %}' class='btn btn-outline-success btn-block'>Revenir</a></div>"),
                HTML("<button type='submit' class='col-lg-3 col-sm-3 btn btn-primary btn-outline-block', >Réserver</button>"),
            ),
        )

class ModReservationForm(forms.Form):
    nbreine = forms.IntegerField(label = 'Nombre reines', required = True,widget=forms.TextInput(attrs={'class': 'form-control'}))
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_arguments = kwargs.get('initial', None)

        self.datedepot = initial_arguments.get('la_date',None)
        self.datechoix = initial_arguments.get('choix_date',None)
        self.resa = initial_arguments.get('la_resa',None)
        self.parAdmin = initial_arguments.get('par_admin',None)
        self.strurlEntrees = "'listentrees'" + ' ' + "'" + self.datedepot.isoformat() + "'" 

        
        #self.fields['nbreine'] = forms.IntegerField(label = 'Nombre reines', required = True, initial = self.resa.nbreine)

        self.fields['datedepot'] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class': 'form-control'},format=('%Y-%m-%d')),initial=self.datedepot, disabled = True)
        self.fields['dateretrait'] = forms.ChoiceField(choices = self.datechoix,widget=forms.Select(attrs={'class': 'form-control'})) 

        self.fields['nbtypfecond1'] = forms.IntegerField(label = 'Nombre Apidéa/Kieler  ', required = True,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['nbtypfecond2'] = forms.IntegerField(label = 'Nombre MiniPlus       ', required = True,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['nbtypfecond3'] = forms.IntegerField(label = 'Nombre Warré          ', required = True,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['nbtypfecond4'] = forms.IntegerField(label = 'Nombre Ruchette-dadant', required = True,widget=forms.TextInput(attrs={'class': 'form-control'}))

        self.fields["nbreine"].initial = self.resa.nbreine
        self.fields['datedepot'].initial = self.resa.datedepot
        self.fields['dateretrait'].initial = self.resa.dateretrait
        self.fields['nbtypfecond1'].initial = self.resa.nbtypfecond1
        self.fields['nbtypfecond2'].initial = self.resa.nbtypfecond2
        self.fields['nbtypfecond3'].initial = self.resa.nbtypfecond3
        self.fields['nbtypfecond4'].initial = self.resa.nbtypfecond4
        
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row (Column('nbreine', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('datedepot', css_class='form-group col-md-3 mb-0'),
                Column('dateretrait', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('nbtypfecond1', css_class='form-group col-lg-3 col-md-6 mb-0'),
                Column('nbtypfecond2', css_class='form-group col-lg-3 col-md-6 mb-0'),
                Column('nbtypfecond3', css_class='form-group col-lg-3 col-md-6 mb-0'),
                Column('nbtypfecond4', css_class='form-group col-lg-3 col-md-6 mb-0'),
            ),
            HTML("<br>"),
        )

        if self.parAdmin:
            self.helper.layout.append(
                            Row(
                        HTML("<div class='col-lg-3 col-sm-3'><a href='{% url " + self.strurlEntrees + " %}' class='btn btn-success btn-block'>Revenir</a></div>"),
                        HTML("<button type='submit' class='col-lg-3 col-sm-3 btn btn-outline-primary btn-block', >Modifier</button>"),
                    ),

            )
        else:
            self.helper.layout.append(            
                Row(
                        HTML("<div class='col-lg-3 col-sm-3'><a href='{% url 'listresas'  %}' class='btn btn-outline-success btn-block'>Revenir</a></div>"),
                        HTML("<button type='submit' class='col-lg-3 col-sm-3 btn btn-outline-primary btn-block', >Modifier</button>"),
                    ),
        )



class ModEntreeReelleForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_arguments = kwargs.get('initial', None)

        self.resa = initial_arguments.get('la_resa',None)
        
        #self.fields['nbreine'] = forms.IntegerField(label = 'Nombre reines', required = True, initial = self.resa.nbreine)

        self.fields['nbreinedepot'] = forms.IntegerField(label = 'Nb reines  ', required = True,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['nbdepotfecond1'] = forms.IntegerField(label = 'Nb Apidéa/Kieler  ', required = True,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['nbdepotfecond2'] = forms.IntegerField(label = 'Nb MiniPlus       ', required = True,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['nbdepotfecond3'] = forms.IntegerField(label = 'Nb Warré          ', required = True,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['nbdepotfecond4'] = forms.IntegerField(label = 'Nb Ruchette-dadant', required = True,widget=forms.TextInput(attrs={'class': 'form-control'}))

        self.fields["nbreinedepot"].initial = self.resa.nbreinedepot
        self.fields['nbdepotfecond1'].initial = self.resa.nbtypfecond1
        self.fields['nbdepotfecond2'].initial = self.resa.nbdepotfecond2
        self.fields['nbdepotfecond3'].initial = self.resa.nbdepotfecond3
        self.fields['nbdepotfecond4'].initial = self.resa.nbdepotfecond4
        print(self.resa.datedepot)
        print(str(self.resa.datedepot))
        self.depot = str(self.resa.datedepot)
        self.strurl = "'listentrees'" + ' ' + "'" + self.depot + "'" 

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nbreinedepot', css_class='form-group col-lg-2 col-md-3 mb-0'),
                Column('nbdepotfecond1', css_class='form-group col-lg-2 col-md-6 mb-0'),
                Column('nbdepotfecond2', css_class='form-group col-lg-2 col-md-6 mb-0'),
                Column('nbdepotfecond3', css_class='form-group col-lg-2 col-md-6 mb-0'),
                Column('nbdepotfecond4', css_class='form-group col-lg-2 col-md-6 mb-0'),
            ),
            HTML("<br>"),
            Row(
                HTML("<div class='col-lg-3 col-sm-3'><a href='{% url " + self.strurl + " %}' class='btn btn-outline-success btn-block'>Revenir</a></div>"),
                HTML("<button type='submit' class='col-lg-3 col-sm-3 btn btn-outline-primary btn-block', >Modifier</button>"),
            ),
         
        )
 
class NewEvenementForm(forms.Form):
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_arguments = kwargs.get('initial', None)

        #self.fields['date'] = forms.DateTimeField(input_formats = ['%d-%m-%Y %H:%M'],widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'},format=('%d-%m-%Y %H:%M')),initial=datetime.now, label = 'date heure' )
        #self.fields['date'] = forms.DateTimeField(input_formats=['%d/%m/%y %H:%M'],widget=forms.DateTimeInput(attrs={'class': 'form-control','type':'datetime-local'},format=('%d-%m-%y %H:%M')), label = 'date fheure' )
        #self.fields['date'] = forms.DateTimeField(input_formats = ['%d-%m-%Y %H:%M'],widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),initial=datetime.now, label = 'date fheure' )
        self.fields['date'] = forms.DateTimeField(input_formats=['%d/%m/%y %H:%M'],widget=forms.TextInput(attrs={'class': 'form-control'}),label = 'date JJ/MM/AA HH:MN')
        self.fields['adresse1'] = forms.CharField(max_length=40, label = 'adresse1', required = False,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['adresse2'] = forms.CharField(max_length=40, label = 'adresse2', required = False,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['codepostal'] = forms.IntegerField(label = 'code postal', required = False,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['ville'] = forms.CharField(max_length=35, label = 'ville', required = False,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['intitule'] = forms.CharField(max_length=100, label = 'intitulé', required = True,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['nombremax'] = forms.IntegerField(label = 'nombre participants max', required = True,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['intitule'] = forms.CharField(max_length=100, label = 'intitulé', required = True,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['programme'] = forms.CharField(required=False,widget=forms.Textarea(attrs={'placeholder': 'Programme','rows':4, 'cols':80,'class': 'form-control'}))
        self.fields['natmail1'] = forms.ModelChoiceField(queryset=TypEmail.objects.all(), label = 'type mailing 1', required = False,widget=forms.Select(attrs={'class': 'form-control'}))
        #pres_CR = forms.ModelChoiceField(required=False, queryset=TypCR.objects.all(), label = 'Cellules Royales')

        self.fields['destmail1'] = forms.ChoiceField(choices = Evenement.LDESTMAIL, label = 'type destinataire 1', required = False,widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['datemail1'] = forms.DateField(input_formats=['%d/%m/%y'],widget=forms.DateInput(attrs={'class': 'form-control'},format = '%d/%m/%y'),label = 'date mail 1 JJ/MM/AA',required=False)
        #self.fields['natmail2'] = forms.ChoiceField(choices = Evenement.LNATMAIL, label = 'type mailing 2', required = False,widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['natmail2'] = forms.ModelChoiceField(queryset=TypEmail.objects.all(), label = 'type mailing 2', required = False,widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['destmail2'] = forms.ChoiceField(choices = Evenement.LDESTMAIL, label = 'type destinataire 2', required = False,widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['datemail2'] = forms.DateField(input_formats=['%d/%m/%y'],widget=forms.DateInput(attrs={'class': 'form-control'},format = '%d/%m/%y'),label = 'date mail 2 JJ/MM/AA',required=False)
         
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('date', css_class='form-group col-md-3 mb-0'),
                Column('nombremax', css_class='form-group col-md-3 mb-0'),
                Column('intitule', css_class='form-group col-md-12 mb-0'),

            ),
            'programme','adresse1','adresse2',
           Row(
                Column('codepostal', css_class='form-group col-md-3 mb-0'),
                Column('ville', css_class='form-group col-md-9 mb-0'),
             ),
            Row(
                Column('datemail1', css_class='form-group col-md-3 mb-0'),
                Column('natmail1', css_class='form-group col-md-3 mb-0'),
                Column('destmail1', css_class='form-group col-md-3 mb-0'),
             ),
            Row(
                Column('datemail2', css_class='form-group col-md-3 mb-0'),
                Column('natmail2', css_class='form-group col-md-3 mb-0'),
                Column('destmail2', css_class='form-group col-md-3 mb-0'),

            ),

            HTML("<br>"),
            Submit('submit', 'Créer')
        )
        
        
        

class ModEvenementForm(forms.Form):
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_arguments = kwargs.get('initial', None)
        self.evt = initial_arguments.get('le_evt',None)
         
        self.fields['date'] = forms.DateTimeField(input_formats=['%d/%m/%y %H:%M'],widget=forms.DateTimeInput(attrs={'class': 'form-control'},format = '%d/%m/%y %H:%M'),label = 'date JJ/MM/AA HH:MN')
        self.fields['adresse1'] = forms.CharField(max_length=40, label = 'adresse1', required = False,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['adresse2'] = forms.CharField(max_length=40, label = 'adresse2', required = False,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['codepostal'] = forms.IntegerField(label = 'code postal', required = False,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['ville'] = forms.CharField(max_length=35, label = 'ville', required = False,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['intitule'] = forms.CharField(max_length=100, label = 'intitulé', required = True,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['nombremax'] = forms.IntegerField(label = 'nombre participants max', required = True,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['intitule'] = forms.CharField(max_length=100, label = 'intitulé', required = True,widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['programme'] = forms.CharField(required=False,widget=forms.Textarea(attrs={'placeholder': 'Programme','rows':4, 'cols':80,'class': 'form-control'}))
        self.fields['natmail1'] = forms.ModelChoiceField(queryset=TypEmail.objects.all(), label = 'type mailing 1', required = False,widget=forms.Select(attrs={'class': 'form-control'}))

        self.fields['destmail1'] = forms.ChoiceField(choices = Evenement.LDESTMAIL, label = 'type destinataire 1', required = False,widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['datemail1'] = forms.DateField(input_formats=['%d/%m/%y'],widget=forms.DateInput(attrs={'class': 'form-control'},format = '%d/%m/%y'),label = 'date mail1 JJ/MM/AA', required = False)
        self.fields['natmail2'] = forms.ModelChoiceField(queryset=TypEmail.objects.all(), label = 'type mailing 2', required = False,widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['destmail2'] = forms.ChoiceField(choices = Evenement.LDESTMAIL, label = 'type destinataire 1', required = False,widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['datemail2'] = forms.DateField(input_formats=['%d/%m/%y'],widget=forms.DateInput(attrs={'class': 'form-control'},format = '%d/%m/%y'),label = 'date mail2 JJ/MM/AA', required = False)

        self.fields["date"].initial = self.evt.date
        self.fields["adresse1"].initial = self.evt.adresse1
        self.fields["adresse2"].initial = self.evt.adresse2
        self.fields["codepostal"].initial = self.evt.codepostal
        self.fields["ville"].initial = self.evt.ville
        self.fields["intitule"].initial = self.evt.intitule
        self.fields["nombremax"].initial = self.evt.nombremax
        self.fields["programme"].initial = self.evt.programme
        self.fields["natmail1"].initial = self.evt.natmail1
        self.fields["destmail1"].initial = self.evt.destmail1
        self.fields["datemail1"].initial = self.evt.datemail1
        self.fields["natmail2"].initial = self.evt.natmail2
        self.fields["destmail2"].initial = self.evt.destmail2
        self.fields["datemail2"].initial = self.evt.datemail2
         
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('date', css_class='form-group col-md-3 mb-0'),
                Column('nombremax', css_class='form-group col-md-3 mb-0'),
                Column('intitule', css_class='form-group col-md-12 mb-0'),

            ),
            'programme','adresse1','adresse2',
           Row(
                Column('codepostal', css_class='form-group col-md-3 mb-0'),
                Column('ville', css_class='form-group col-md-9 mb-0'),
             ),
            Row(
                Column('datemail1', css_class='form-group col-md-3 mb-0'),
                Column('natmail1', css_class='form-group col-md-3 mb-0'),
                Column('destmail1', css_class='form-group col-md-3 mb-0'),
             ),
            Row(
                Column('datemail2', css_class='form-group col-md-3 mb-0'),
                Column('natmail2', css_class='form-group col-md-3 mb-0'),
                Column('destmail2', css_class='form-group col-md-3 mb-0'),

            ),

            HTML("<br>"),
            Submit('submit', 'Modifier')
        )
        
        

class NewInscriptionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        self.helper = FormHelper()
        self.helper.layout = Layout(
             HTML("<br>"), 
             Row(
                HTML("<div class='col-lg-3 col-sm-3'><a href='{% url 'listevtsmembre'  %}' class='btn btn-outline-success btn-block'>Revenir</a></div>"),
                HTML("<button type='submit' class='col-lg-3 col-sm-3 btn btn-outline-primary btn-block', >Inscription</button>"),
                
            ),

        )
