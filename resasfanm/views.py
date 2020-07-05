from django.http import Http404
from django.http import HttpResponse, FileResponse
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.mixins import LoginRequiredMixin



from datetime import datetime
from resasfanm.models import Reservation, Capacite, Presence
from django.contrib.auth.models import User

from django.urls import reverse_lazy
from django.views import generic

from .forms import NewReservationForm
from datetime import timedelta 
import datetime
#from io import BytesIO, StringIO
#from csv import writer,QUOTE_ALL
#import csv
#from zipfile import ZipFile


#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import A4
#from reportlab.lib import colors
#from reportlab.lib.units import mm, inch
#from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
#from reportlab.lib.styles import getSampleStyleSheet
#from reportlab.rl_config import defaultPageSize

# Create your views here.
def home(request):
	return render(request, 'resasfanm/home.html')
	


@login_required
def newresa(request,idcapa):
	msg =''
	capa = Capacite.objects.get(id=idcapa)
	datededepot = capa.datecapa
	dateret1 = datededepot + timedelta(days=14)
	dateret2 = dateret1 + timedelta(days=7)
	if Capacite.objects.filter(datecapa=dateret2).exists():
		datechoix = ((dateret1 , dateret1),(dateret2, dateret2))
	else:
		print('j y pass')
		datechoix = ((dateret1 , dateret1),(dateret1 , dateret1))
		
#	datechoix = (("1", dateret1),("2", dateret2))
#	datechoix = ((dateret1 , dateret1),(dateret2, dateret2))

	if request.method == 'POST':
		form = NewReservationForm(request.POST, initial={'la_date' : datededepot, 'choix_date' : datechoix})
		if form.is_valid():
			nbreinedemand = form.cleaned_data['nbreine']
			dated = datededepot				
			datert = datetime.datetime.strptime(form.cleaned_data['dateretrait'], "%Y-%m-%d").date()
			resaok = True
			while (dated < datert):
				capac = Capacite.objects.filter(datecapa = dated).first()
				if (capac.get_reinesdispos() < nbreinedemand):
					resaok = False
					msg += 'Manque de capacité à la station le ' + dated.strftime("%d/%m/%Y")
				dated = dated + timedelta(days=7)
					
			if (resaok):
				reservation = Reservation()
				reservation.apiculteur = request.user.apiculteur
				reservation.nbreine = form.cleaned_data['nbreine']
				reservation.datedepot = form.cleaned_data['datedepot']
				reservation.dateretrait = form.cleaned_data['dateretrait']
				reservation.nbtypfecond1 = form.cleaned_data['nbtypfecond1']
				reservation.nbtypfecond2 = form.cleaned_data['nbtypfecond2']
				reservation.nbtypfecond3 = form.cleaned_data['nbtypfecond3']
				reservation.nbtypfecond4 = form.cleaned_data['nbtypfecond4']
				dated = datededepot				
				#try:
				reservation.save()
				dater = datetime.datetime.strptime(reservation.dateretrait, "%Y-%m-%d").date()
				while (dated < dater):
					present = Presence()
					capac = Capacite.objects.filter(datecapa = dated).first()
					present.capa = capac
					present.resa = reservation
					present.save()
					dated = dated + timedelta(days=7)
				return redirect('listresas')  # TODO: redirect to the created topic page
	else:
		form = NewReservationForm(initial={'la_date' : datededepot, 'choix_date' : datechoix})
	return render(request, 'resasfanm/newresa.html', {'form': form, 'mod' : False, 'msg' : msg})

@login_required	
def listcapacites(request):
# affiche les dates sur lesquelles l'apiculteur n'a pas réservé
	datesreservees = Reservation.objects.filter(apiculteur=request.user.apiculteur).values_list('datedepot',flat = True)
	capacites = Capacite.objects.filter(depotpossible=True).exclude(datecapa__in=datesreservees)
	return render(request, 'resasfanm/capacites.html', {'les_capacites':capacites})

@login_required
def listresas(request):
	resas = Reservation.objects.filter(apiculteur=request.user.apiculteur).order_by('datedepot')
	return render(request, 'resasfanm/listresas.html', {'les_resas':resas})

@login_required
def listgestion(request):
	capacites = Capacite.objects.all()
	return render(request, 'resasfanm/listgestion.html', {'les_capacites':capacites})

@login_required	
def listentrees(request,dateentree):
	datee = datetime.datetime.strptime(dateentree, "%Y-%m-%d").date()
	resas = Reservation.objects.filter(datedepot=datee)

	return render(request, 'resasfanm/listentrees.html', {'les_resas':resas, 'date_entree': datee})

@login_required
def listsorties(request,datesortie):
	dates = datetime.datetime.strptime(datesortie, "%Y-%m-%d").date()
	resas = Reservation.objects.filter(dateretrait=dates)

	return render(request, 'resasfanm/listsorties.html', {'les_resas':resas, 'date_sortie': dates})
	
	
