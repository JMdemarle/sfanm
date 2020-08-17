from django.http import Http404
from django.http import HttpResponse, FileResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.db.models import Exists, Value, BooleanField

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import date, datetime

#from django.contrib.auth.mixins import LoginRequiredMixin



from resasfanm.models import Reservation, Capacite, Presence, Evenement, Inscription
from django.contrib.auth.models import User

from django.urls import reverse_lazy
from django.views import generic

from .forms import NewReservationForm, ModReservationForm, NewEvenementForm, ModEvenementForm, NewInscriptionForm
from datetime import timedelta 
import datetime

from io import BytesIO, StringIO
#from csv import writer,QUOTE_ALL
#import csv
#from zipfile import ZipFile

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize

# Create your views here.
#@login_required
def home(request):
	'''	username = request.META.get('REMOTE_USER_VAR')
	for el in request.META:
		print(el)
		print(request.META[el])
	#password = request.GET.get('password')
	msg = username
	print(username)
	#print(password)'''
	
	msg = ''
	if (request.user.is_staff):
		return render(request, 'resasfanm/home.html', {'msg' : msg})
	else:
#		return redirect('listresas') 
		return render(request, 'resasfanm/maintenance.html')


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
		datechoix = ((dateret1 , dateret1),(dateret1 , dateret1))
		
	if request.method == 'POST':
		form = NewReservationForm(request.POST, initial={'la_date' : datededepot, 'choix_date' : datechoix})
		if form.is_valid():
			nbreinedemand = form.cleaned_data['nbreine']
			dated = datededepot				
			datert = datetime.datetime.strptime(form.cleaned_data['dateretrait'], "%Y-%m-%d").date()
			# vérification des capacités
			resaok = True
			while (dated < datert):
				capac = Capacite.objects.filter(datecapa = dated).first()
				if (capac.get_reinesdispos() < nbreinedemand):
					resaok = False
					msg += 'Manque de capacité à la station le ' + dated.strftime("%d/%m/%Y")
				dated = dated + timedelta(days=7)
			if nbreinedemand > request.user.nbreinesmax:
				resaok = False
				msg += 'Vous dépassez votre quotat de ' + str(request.user.nbreinesmax) + ' reines'	
			if (resaok):
				reservation = Reservation()
				reservation.apiculteur = request.user
				reservation.nbreine = form.cleaned_data['nbreine']
				reservation.datedepot = form.cleaned_data['datedepot']
				reservation.dateretrait = form.cleaned_data['dateretrait']
				reservation.nbtypfecond1 = form.cleaned_data['nbtypfecond1']
				reservation.nbtypfecond2 = form.cleaned_data['nbtypfecond2']
				reservation.nbtypfecond3 = form.cleaned_data['nbtypfecond3']
				reservation.nbtypfecond4 = form.cleaned_data['nbtypfecond4']
				dated = datededepot				
				#
				reservation.save()
				dater = datetime.datetime.strptime(reservation.dateretrait, "%Y-%m-%d").date()
				# mise à jour des présences
				while (dated < dater):
					present = Presence()
					capac = Capacite.objects.filter(datecapa = dated).first()
					present.capa = capac
					present.resa = reservation
					present.save()
					dated = dated + timedelta(days=7)
				subject = 'SFANM - Confirmation de réservation'
				html_message = render_to_string('resasfanm/mailconfirmationreservation.html', {'la_resa': reservation})
				#plain_message = strip_tags(html_message)
				from_email = 'SFANM <contact@sfanm.fr>'
				to = request.user.email
				#mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)			
				mail.send_mail(subject, html_message, from_email, [to])				

				return redirect('listresas')  # TODO: redirect to the created topic page
	else:
		form = NewReservationForm(initial={'la_date' : datededepot, 'choix_date' : datechoix})
	return render(request, 'resasfanm/newresa.html', {'form': form, 'mod' : False, 'msg' : msg})

# Modification rerservation
def modresa(request,idresa):
	msg =''
	resam = Reservation.objects.get(id=idresa)
	print(resam.nbreine)
	datededepot = resam.datedepot
	dateret1 = datededepot + timedelta(days=14)
	dateret2 = dateret1 + timedelta(days=7)
	if Capacite.objects.filter(datecapa=dateret2).exists():
		datechoix = ((dateret1 , dateret1),(dateret2, dateret2))
	else:
		datechoix = ((dateret1 , dateret1),(dateret1 , dateret1))

	form = ModReservationForm(request.POST, initial={'la_date' : datededepot, 'choix_date' : datechoix,'la_resa' : resam})

	if form.is_valid():
		nbreinedemand = form.cleaned_data['nbreine']
		dated = datededepot				
		datert = datetime.datetime.strptime(form.cleaned_data['dateretrait'], "%Y-%m-%d").date()
		# vérification des capacités
		resaok = True
		while (dated < datert):
			capac = Capacite.objects.filter(datecapa = dated).first()
			if (capac.get_reinesdispos() < nbreinedemand):
				resaok = False
				msg += 'Manque de capacité à la station le ' + dated.strftime("%d/%m/%Y")
			dated = dated + timedelta(days=7)
			print(dated)
		if nbreinedemand > request.user.nbreinesmax:
			resaok = False
			msg += 'Vous dépassez votre quotat de ' + str(request.user.nbreinesmax) + ' reines'	
		if (resaok):
			#reservation = Reservation()
			resam.apiculteur = request.user
			resam.nbreine = form.cleaned_data['nbreine']
			resam.datedepot = form.cleaned_data['datedepot']
			resam.dateretrait = form.cleaned_data['dateretrait']
			resam.nbtypfecond1 = form.cleaned_data['nbtypfecond1']
			resam.nbtypfecond2 = form.cleaned_data['nbtypfecond2']
			resam.nbtypfecond3 = form.cleaned_data['nbtypfecond3']
			resam.nbtypfecond4 = form.cleaned_data['nbtypfecond4']
			dated = datededepot				
			#
			resam.save()
			dater = datetime.datetime.strptime(resam.dateretrait, "%Y-%m-%d").date()
				# mise à jour des présences
			# Etape 1 = supression
			Presence.objects.filter(resa = resam).delete()
			# Etape 2 = création à nouveau
			while (dated < dater):
				present = Presence()
				capac = Capacite.objects.filter(datecapa = dated).first()
				present.capa = capac
				present.resa = resam
				present.save()
				dated = dated + timedelta(days=7)
			subject = 'SFANM - Confirmation modification de réservation'
			html_message = render_to_string('resasfanm/mailconfirmationreservation.html', {'la_resa': resam})
			#plain_message = strip_tags(html_message)
			from_email = 'SFANM <contact@sfanm.fr>'
			to = request.user.email
			#mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)			
			mail.send_mail(subject, html_message, from_email, [to])				
				
			return redirect('listresas')  
	else:
		form = ModReservationForm(initial={'la_date' : datededepot, 'choix_date' : datechoix,'la_resa' : resam})
	return render(request, 'resasfanm/newresa.html', {'form': form, 'mod' : True, 'msg' : msg})

@login_required	
def affpourdelresa(request,idresa):
	resam = Reservation.objects.get(id=idresa)
	return render(request, 'resasfanm/affpourdelresa.html', {'la_resa': resam})

@login_required	
def delresa(request,idresa):
	resam = Reservation.objects.get(id=idresa)
	subject = 'SFANM - Confirmation d"annulation de réservation'
	html_message = render_to_string('resasfanm/mailconfirmationannulreservation.html', {'la_resa': resam})
	#plain_message = strip_tags(html_message)
	from_email = 'SFANM <contact@sfanm.fr>'
	to = request.user.email
	#mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)			
	mail.send_mail(subject, html_message, from_email, [to])				
	resam.delete()
	return redirect('listresas')  
	
@login_required	
def listcapacites(request):
# affiche les dates sur lesquelles l'apiculteur n'a pas réservé
	datesreservees = Reservation.objects.filter(apiculteur=request.user).values_list('datedepot',flat = True)
	capacites = Capacite.objects.filter(depotpossible=True).filter(datecapa__gt = date.today()).exclude(datecapa__in=datesreservees)
	return render(request, 'resasfanm/capacites.html', {'les_capacites':capacites})

@login_required
def listresas(request):
#  affiche les réservations de l'apiculteur et les évènements	
	resas = Reservation.objects.filter(apiculteur=request.user).order_by('datedepot')
	#inscrita = Inscription.objects.filter(apiculteur=request.user)
	#touslesevts = Evenement.objects.filter(date__gte = date.today())
	#evtsinscrits = Evenement.objects.filter(date__gte = date.today(),partevts__apiculteur=request.user)
	#evtspasinscrits = touslesevts.difference(evtsinscrits)
	#evtsinscrits.annotate(estinscrit=Value(True, BooleanField()))
	#evtspasinscrits.annotate(estinscrit=Value(False, BooleanField()))
	#evts = evtspasinscrits.union(evtsinscrits).order_by('date')
	evts = Evenement.objects.filter(date__gte = date.today()).order_by('date')
	for evt in evts:
		if Inscription.objects.filter(evenement=evt,apiculteur=request.user).exists():
			evt.estinscrit=True
		else:
			evt.estinscrit=False
			
	return render(request, 'resasfanm/listresas.html', {'les_resas':resas,'les_evts':evts})

@login_required
@staff_member_required
def listgestion(request):
	capacites = Capacite.objects.all()
	return render(request, 'resasfanm/listgestion.html', {'les_capacites':capacites})

@login_required	
@staff_member_required
def listentrees(request,dateentree):
	datee = datetime.datetime.strptime(dateentree, "%Y-%m-%d").date()
	resas = Reservation.objects.filter(datedepot=datee)

	return render(request, 'resasfanm/listentrees.html', {'les_resas':resas, 'date_entree': datee})

@login_required
@staff_member_required
def listsorties(request,datesortie):
	dates = datetime.datetime.strptime(datesortie, "%Y-%m-%d").date()
	resas = Reservation.objects.filter(dateretrait=dates)

	return render(request, 'resasfanm/listsorties.html', {'les_resas':resas, 'date_sortie': dates})
	
def editentreesortie(request,dateedit):
	PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
	styles = getSampleStyleSheet()

	def myFirstPage(canvas, doc):
		canvas.saveState()
		canvas.setFont('Times-Bold',16)
		canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-20, Title)
		canvas.setFont('Times-Roman',9)
		canvas.drawString(inch, 0.25 * inch, "Première / %s" % pageinfo)
		canvas.restoreState()

	def myLaterPages(canvas, doc):
		canvas.saveState()
		canvas.setFont('Times-Roman',9)
		canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))
		canvas.restoreState()
	
	pdf_buffer = BytesIO()
	doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, leftMargin=15*mm,topMargin=10*mm, bottomMargin=1*mm)	
	#doc = SimpleDocTemplate("/tmp/somefilename.pdf", pagesize=A4, topMargin=5*mm, bottomMargin=1*mm)
	Story = []
	style = styles["Normal"]
	Title = "Entrées et sorties du " + dateedit
	pageinfo = "gestion SFANM"

	Story.append(Spacer(1, 10*mm))
	
	ptext = '<font size="12"><u>Les entrées </u></font>'
	Story.append(Paragraph(ptext, styles["Normal"]))

	Story.append(Spacer(1, 10*mm))
	
	
	datee = datetime.datetime.strptime(dateedit, "%Y-%m-%d").date()
	resas = Reservation.objects.filter(datedepot=datee).order_by('apiculteur__nom')
	
# Make heading for each column and start data list
	data = [['Apicuteur','Prénom','téléphone','Nb reines','Nb ruches','Présent']]
# Assemble data for each column using simple loop to append it into data list
	for resa in resas:
		data.append([resa.apiculteur.nom,resa.apiculteur.prenom, resa.apiculteur.telephone,resa.nbreine,resa.nbruches,''])

	tableThatSplitsOverPages = Table(data, colWidths=(45*mm,40*mm,30*mm,30*mm, 20*mm, 20*mm),rowHeights=(10*mm), repeatRows=1)
	tableThatSplitsOverPages.hAlign = 'LEFT'
	tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
		('VALIGN',(0,0),(-1,-1),'TOP'),
		('LINEBELOW',(0,0),(-1,-1),1,colors.black),
		('GRID',(0,0),(-1,-1),1,colors.black)])
	tableThatSplitsOverPages.setStyle(tblStyle)
	Story.append(tableThatSplitsOverPages)
	
	Story.append(PageBreak())

	Story.append(Spacer(1, 10*mm))
	
	ptext = '<font size="12"><u>Les sorties </u></font>'
	Story.append(Paragraph(ptext, styles["Normal"]))

	Story.append(Spacer(1, 10*mm))
	

	resas = Reservation.objects.filter(dateretrait=datee).order_by('apiculteur__nom')
	
# Make heading for each column and start data list
	data = [['Apicuteur','Prénom','téléphone','Nb reines','Nb ruches','Présent']]
# Assemble data for each column using simple loop to append it into data list
	for resa in resas:
		data.append([resa.apiculteur.nom,resa.apiculteur.prenom, resa.apiculteur.telephone,resa.nbreine,resa.nbruches,''])

	tableThatSplitsOverPages = Table(data, colWidths=(45*mm,40*mm,30*mm,30*mm, 20*mm, 20*mm),rowHeights=(10*mm), repeatRows=1)
	tableThatSplitsOverPages.hAlign = 'LEFT'
	tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
		('VALIGN',(0,0),(-1,-1),'TOP'),
		('LINEBELOW',(0,0),(-1,-1),1,colors.black),
		('GRID',(0,0),(-1,-1),1,colors.black)])
	tableThatSplitsOverPages.setStyle(tblStyle)
	Story.append(tableThatSplitsOverPages)
		
	doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


	pdf_buffer.seek(0)
#	return FileResponse(pdf_buffer, as_attachment=True, filename='hello.pdf')
	pdf = pdf_buffer.getvalue()
	pdf_buffer.close()
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'
	response.write(pdf)

	return response

	return redirect('listgestion')

@login_required	
@staff_member_required
def newevenement(request):
	msg = ''
	if request.method == 'POST':
		form = NewEvenementForm(request.POST)
		if form.is_valid():
			evt = Evenement()
			
			evt.date = form.cleaned_data['date']
			evt.adresse1 = form.cleaned_data['adresse1']
			evt.adresse2 = form.cleaned_data['adresse2']
			evt.codepostal = form.cleaned_data['codepostal']
			evt.ville = form.cleaned_data['ville']
			evt.nombremax = form.cleaned_data['nombremax']
			evt.intitule = form.cleaned_data['intitule']
			evt.programme = form.cleaned_data['programme']
			evt.natmail1 = form.cleaned_data['natmail1']
			evt.datemail1 = form.cleaned_data['datemail1']
			evt.destmail1 = form.cleaned_data['destmail1']
			evt.natmail2 = form.cleaned_data['natmail2']
			evt.datemail2 = form.cleaned_data['datemail2']
			evt.destmail2 = form.cleaned_data['destmail2']
			evt.save()
			try:
				evt.save()
				return redirect('listevenements')  
			except:
				msg = 'ce nom existe deja'
	else:
		form = NewEvenementForm()
	return render(request, 'resasfanm/new_evenement.html', {'form': form, 'mod' : False, 'msg' : msg})

@login_required	
@staff_member_required
def modevenement(request,idevt):
	msg = ''
	evtm = Evenement.objects.get(id=idevt)
	print(evtm.intitule)

	form = ModEvenementForm(request.POST, initial={'le_evt' : evtm})
	if request.method == 'POST':
		form = NewEvenementForm(request.POST)
		if form.is_valid():
			
			evtm.date = form.cleaned_data['date']
			evtm.adresse1 = form.cleaned_data['adresse1']
			evtm.adresse2 = form.cleaned_data['adresse2']
			evtm.codepostal = form.cleaned_data['codepostal']
			evtm.ville = form.cleaned_data['ville']
			evtm.nombremax = form.cleaned_data['nombremax']
			evtm.intitule = form.cleaned_data['intitule']
			evtm.programme = form.cleaned_data['programme']
			evtm.natmail1 = form.cleaned_data['natmail1']
			evtm.datemail1 = form.cleaned_data['datemail1']
			evtm.destmail1 = form.cleaned_data['destmail1']			
			evtm.natmail2 = form.cleaned_data['natmail2']
			evtm.datemail2 = form.cleaned_data['datemail2']
			evtm.destmail2 = form.cleaned_data['destmail2']
			try:
				evtm.save()
				return redirect('listevenements')  
			except:
				msg = 'ce nom existe deja'
	else:
		form = ModEvenementForm(initial={'le_evt' : evtm})
	return render(request, 'resasfanm/new_evenement.html', {'form': form, 'mod' : True, 'msg' : msg})

@login_required	
@staff_member_required
def listevenements(request):
	evts = Evenement.objects.filter(date__gt = date.today())
	return render(request, 'resasfanm/listevenements.html', {'les_evts':evts})

@login_required
def newinscription(request,idevt):
	msg =''
	evt = Evenement.objects.get(id=idevt)
		
	if request.method == 'POST':
		form = NewInscriptionForm(request.POST, initial={'le_evt' : evt})
		if "cancel" in request.POST:
			return redirect('listresas') 
		else:
			if form.is_valid():
				#while (dated < datert):
			#		capac = Capacite.objects.filter(datecapa = dated).first()
			#		if (capac.get_reinesdispos() < nbreinedemand):
			#			resaok = False
			#			msg += 'Manque de capacité à la station le ' + dated.strftime("%d/%m/%Y")
			#		dated = dated + timedelta(days=7)
				inscriok = True
				if (inscriok):
					inscription = Inscription()
					inscription.apiculteur = request.user
					inscription.evenement = evt
					inscription.save()
					subject = 'SFANM - Confirmation d"inscription'
					html_message = render_to_string('resasfanm/mailconfirmationinscription.html', {'le_evt': evt})
					#plain_message = strip_tags(html_message)
					from_email = 'SFANM <contact@sfanm.fr>'
					to = request.user.email
					#mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)			
					mail.send_mail(subject, html_message, from_email, [to])				

					return redirect('listresas')  # TODO: redirect to the created topic page
	else:
		form = NewInscriptionForm()
	return render(request, 'resasfanm/new_inscription.html', {'form': form, 'mod' : False, 'msg' : msg, 'le_evt' : evt})

@login_required	
def affpourdelinscription(request,idevt):
	evt = Evenement.objects.get(id=idevt)
	return render(request, 'resasfanm/affpourdelinscrit.html', {'le_evt': evt})

@login_required		
def delinscription(request,idevt):
	#evt = Evenement.objects.get(id=idevt)
	inscript = Inscription.objects.get(evenement=idevt,apiculteur=request.user.id)
	subject = 'SFANM - Confirmation d"annulation de réservation'
	html_message = render_to_string('resasfanm/mailconfirmationannulinscription.html', {'la_inscript' : inscript})
	#plain_message = strip_tags(html_message)
	from_email = 'SFANM <contact@sfanm.fr>'
	to = request.user.email
	#mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)			
	mail.send_mail(subject, html_message, from_email, [to])				
	inscript.delete()
	return redirect('listresas')  

	#return render(request, 'resasfanm/listresas.html')
	
@login_required	
def voirevt(request,idevt):
	evt = Evenement.objects.get(id=idevt)
	return render(request, 'resasfanm/voirevt.html', {'le_evt': evt})
	
@login_required	
@staff_member_required
def listeparticipants(request,idevt):
	parts = Inscription.objects.filter(evenement=idevt).order_by('apiculteur__nom')
	evt = Evenement.objects.get(id=idevt)
	return render(request, 'resasfanm/listparticipants.html', {'les_parts':parts, 'le_evt':evt})
