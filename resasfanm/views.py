import os
from django.http import Http404
from django.http import HttpResponse, FileResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.templatetags.static import static


from django.db.models import Exists, Value, BooleanField

from django.core import mail
from django.core.mail import EmailMessage

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import date, datetime

#from django.contrib.auth.mixins import LoginRequiredMixin



from resasfanm.models import Reservation, Capacite, Presence, Evenement, Inscription
from users.models import CustomUser

from django.contrib.auth.models import User

from django.urls import reverse_lazy
from django.views import generic

from .forms import NewReservationForm, NewReservationApiForm, ModReservationForm,  NewEvenementForm, ModEvenementForm, NewInscriptionForm, ModEntreeReelleForm
from datetime import timedelta 
import datetime

from io import BytesIO, StringIO
#from csv import writer,QUOTE_ALL
#import csv
#from zipfile import ZipFile

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import mm, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize

# Create your views here.
#@login_required
def home(request):
    ''' username = request.META.get('REMOTE_USER_VAR')
    for el in request.META:
        print(el)
        print(request.META[el])
    #password = request.GET.get('password')
    msg = username
    print(username)
    #print(password)'''
    
    msg = ''
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    else:
        if (request.user.is_staff):
            return render(request, 'resasfanm/home.html', {'msg' : msg})
        else:
#       return redirect('listresas') 
            return render(request, 'resasfanm/maintenance.html')

# réservation créée par admin pour le compte API
@login_required
def newresaapi(request,idcapa):
    msg =''
    capa = Capacite.objects.get(id=idcapa)
    datededepot = capa.datecapa
    libeldepot = capa.libelle
    dateret1 = datededepot + timedelta(days=14)
    lesApis = CustomUser.objects.filter(is_active = True).order_by('nom')
    caparet1 = Capacite.objects.filter(datecapa=dateret1).first()
    if caparet1:
        libelret1 = caparet1.libelle
    else:
    #if not(Capacite.objects.filter(datecapa=dateret1).exists()):
        subject = 'SFANM - Problème de définition des dates de réservation'
        html_message = 'il n est pas possible de retirer les ruches après la date de dépôt'
        from_email = 'SFANM <' + settings.DEFAULT_FROM_EMAIL + '>'
        to = 'contact@sfanm.fr'
        mail.send_mail(subject, html_message, from_email, [to])             

        return render(request, 'resasfanm/resaimpossible.html')
    

        
    dateret2 = dateret1 + timedelta(days=7)
    caparet2 = Capacite.objects.filter(datecapa=dateret2).first()

    if caparet2:
        libelret2 = caparet2.libelle
        datechoix = ((dateret1 , libelret1),(dateret2, libelret2))
    else:
        datechoix = ((dateret1 , libelret1),(dateret1 , libelret1))
        
    if request.method == 'POST':
        form = NewReservationApiForm(request.POST, initial={'la_date' : datededepot, 'lib_depot' : libeldepot, 'choix_date' : datechoix, 'les_apis' : lesApis})
        if form.is_valid():
            nbreinedemand = form.cleaned_data['nbreine']
            dated = datededepot             
            datert = datetime.datetime.strptime(form.cleaned_data['dateretrait'], "%Y-%m-%d").date()
            # vérification des capacités
            resaok = True
            # pas de contrôle car c'est l'admin qui fait
            #while (dated < datert):
            #    capac = Capacite.objects.filter(datecapa = dated).first()
            #    if (capac.get_reinesdispos() < nbreinedemand):
            #        resaok = False
            #        msg += 'Manque de capacité à la station le ' + dated.strftime("%d/%m/%Y")
            #    dated = dated + timedelta(days=7)
            #if nbreinedemand > request.user.nbreinesmax:
            #    resaok = False
            #    msg += 'Vous dépassez votre quotat de ' + str(request.user.nbreinesmax) + ' reines' 
            nbtypfecond1 = form.cleaned_data['nbtypfecond1']
            nbtypfecond2 = form.cleaned_data['nbtypfecond2']
            nbtypfecond3 = form.cleaned_data['nbtypfecond3']
            nbtypfecond4 = form.cleaned_data['nbtypfecond4']
            if (nbtypfecond1 + nbtypfecond2 + nbtypfecond3 + nbtypfecond4) > nbreinedemand:
                resaok = False
                msg += 'Le nombre de ruches est supérieur à celui des reines !  '  
            formApiculteur = form.cleaned_data['apiculteur']
            formDateDepot = datededepot
            if Reservation.objects.filter(apiculteur=formApiculteur, datedepot=formDateDepot).exists():
                resaok = False
                msg += 'L apiculteur a déjà une reservation pour cette date'
            if (resaok):
                reservation = Reservation()
                idapiculteur = formApiculteur
                reservation.apiculteur = CustomUser.objects.get(id=idapiculteur)
                reservation.nbreine = form.cleaned_data['nbreine']
                reservation.datedepot = formDateDepot
                reservation.dateretrait = form.cleaned_data['dateretrait']
                reservation.nbtypfecond1 = form.cleaned_data['nbtypfecond1']
                reservation.nbtypfecond2 = form.cleaned_data['nbtypfecond2']
                reservation.nbtypfecond3 = form.cleaned_data['nbtypfecond3']
                reservation.nbtypfecond4 = form.cleaned_data['nbtypfecond4']
                reservation.nbdepotfecond1 = reservation.nbtypfecond1
                reservation.nbdepotfecond2 = reservation.nbtypfecond2
                reservation.nbdepotfecond3 = reservation.nbtypfecond3
                reservation.nbdepotfecond4 = reservation.nbtypfecond4
                reservation.nbreinedepot = reservation.nbreine                                                
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
                    
                #  Envoi mail
                subject = 'SFANM - Confirmation de réservation'
                html_message = render_to_string('resasfanm/mailconfirmationreservation.html', {'la_resa': reservation, 'le_api': reservation.apiculteur, })
                #plain_message = strip_tags(html_message)
                from_email = 'SFANM <'  + settings.DEFAULT_FROM_EMAIL + '>'
                api = CustomUser.objects.get(id=formApiculteur)
                to = api.email
                pdf = Etiquette(reservation.id)
                try:
                        #mail.send_mail(subject, html_message, from_email, [to])
                    message = EmailMessage(subject=subject,body=html_message,from_email=from_email,to=[to, 'contact@sfanm.fr'])
                    message.attach('etiquettes.pdf', pdf, 'application/pdf')

                except Exception as e: print(e)
                else:
                    print ('message préparé')
            #message.content_subtype = "text/plain"
                    try:
                        message.send() 
                        print('mail envoyé')
                    except:
                        print('pb envoi')

                return redirect('listentrees', datededepot)  
    else:
        form = NewReservationApiForm(initial={'la_date' : datededepot, 'lib_depot' : libeldepot,'choix_date' : datechoix,  'les_apis' : lesApis})
    return render(request, 'resasfanm/newresaapi.html', {'form': form, 'mod' : False, 'msg' : msg, 'date_depot' : datededepot})

@login_required
def newresa(request,idcapa):
    msg =''
    capa = Capacite.objects.get(id=idcapa)
    datededepot = capa.datecapa
    libeldepot = capa.libelle
    print(libeldepot)
    dateret1 = datededepot + timedelta(days=14)
    caparet1 = Capacite.objects.filter(datecapa=dateret1).first()
    if caparet1:
        libelret1 = caparet1.libelle
    else:    
    #if not(Capacite.objects.filter(datecapa=dateret1).exists()):
        subject = 'SFANM - Problème de définition des dates de réservation'
        html_message = 'il n est pas possible de retirer les ruches après la date de dépôt'
        from_email = 'SFANM <' + settings.DEFAULT_FROM_EMAIL + '>'
        to = 'contact@sfanm.fr'
        mail.send_mail(subject, html_message, from_email, [to])             

        return render(request, 'resasfanm/resaimpossible.html')

    # Possibilité de réserver sur 3semaines supprimée    
    #dateret2 = dateret1 + timedelta(days=7)
    #caparet2 = Capacite.objects.filter(datecapa=dateret2    ).first()
    #if caparet2:
    #    libelret2 = caparet2.libelle
    #    datechoix = ((dateret1 , libelret1),(dateret2, libelret2))
    #else:
    datechoix = ((dateret1 , libelret1),(dateret1 , libelret1))
        
    if request.method == 'POST':
        form = NewReservationForm(request.POST, initial={'lib_depot' : libeldepot, 'choix_date' : datechoix})
        if form.is_valid():
            nbreinedemand = form.cleaned_data['nbreine']
            dated = datededepot          
    # Possibilité de réserver sur 3semaines supprimée
            datert = dateret1
            # datert = datetime.datetime.strptime(form.cleaned_data['dateretrait'], "%Y-%m-%d").date()
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
            nbtypfecond1 = form.cleaned_data['nbtypfecond1']
            nbtypfecond2 = form.cleaned_data['nbtypfecond2']
            nbtypfecond3 = form.cleaned_data['nbtypfecond3']
            nbtypfecond4 = form.cleaned_data['nbtypfecond4']
            if (nbtypfecond1 + nbtypfecond2 + nbtypfecond3 + nbtypfecond4) > nbreinedemand:
                resaok = False
                msg += 'Le nombre de ruches est supérieur à celui des reines !  '   

            if (resaok):
                reservation = Reservation()
                reservation.apiculteur = request.user
                reservation.nbreine = form.cleaned_data['nbreine']
                reservation.datedepot = datededepot
    # Possibilité de réserver sur 3semaines supprimée
                print('===> date')
                print(dateret1)
                reservation.dateretrait = dateret1
                #reservation.dateretrait = form.cleaned_data['dateretrait']
                reservation.nbtypfecond1 = form.cleaned_data['nbtypfecond1']
                reservation.nbtypfecond2 = form.cleaned_data['nbtypfecond2']
                reservation.nbtypfecond3 = form.cleaned_data['nbtypfecond3']
                reservation.nbtypfecond4 = form.cleaned_data['nbtypfecond4']
                reservation.nbdepotfecond1 = reservation.nbtypfecond1
                reservation.nbdepotfecond2 = reservation.nbtypfecond2
                reservation.nbdepotfecond3 = reservation.nbtypfecond3
                reservation.nbdepotfecond4 = reservation.nbtypfecond4
                reservation.nbreinedepot = reservation.nbreine                                                
                dated = datededepot             
                #
                reservation.save()
    # Possibilité de réserver sur 3semaines supprimée
                dater = datert
    #            dater = datetime.datetime.strptime(reservation.dateretrait, "%Y-%m-%d").date()
                # mise à jour des présences
                while (dated < dater):
                    present = Presence()
                    capac = Capacite.objects.filter(datecapa = dated).first()
                    present.capa = capac
                    present.resa = reservation
                    present.save()
                    dated = dated + timedelta(days=7)
                    
                #  Envoi mail
                subject = 'SFANM - Confirmation de réservation'
                html_message = render_to_string('resasfanm/mailconfirmationreservation.html', {'la_resa': reservation, 'le_api': reservation.apiculteur})
                #plain_message = strip_tags(html_message)
                from_email = 'SFANM <'  + settings.DEFAULT_FROM_EMAIL + '>'
                to = request.user.email
                pdf = Etiquette(reservation.id)
                try:
                        #mail.send_mail(subject, html_message, from_email, [to])
                    message = EmailMessage(subject=subject,body=html_message,from_email=from_email,to=[to])
                    message.attach('etiquettes.pdf', pdf, 'application/pdf')

                except Exception as e: print(e)
                else:
                    print ('message préparé')
            #message.content_subtype = "text/plain"
                    try:
                        message.send() 
                        print('mail envoyé')
                    except:
                        print('pb envoi')

                return redirect('listresas')  # TODO: redirect to the created topic page
    else:
        form = NewReservationForm(initial={'lib_depot' : libeldepot, 'choix_date' : datechoix})
    return render(request, 'resasfanm/newresa.html', {'form': form, 'mod' : False, 'msg' : msg})

# Modification rerservation pour un apiculteur
@login_required
def modResaApi(request,idresa,idapi):
    msg =''
    resam = Reservation.objects.get(id=idresa)
    api = CustomUser.objects.get(id=idapi)
    nbreineavant = resam.nbreine
    datededepot = resam.datedepot
    libeldepot = Capacite.objects.filter(datecapa=datededepot).first().libelle

    dateret0 = datededepot + timedelta(days=7)
    dateret1 = datededepot + timedelta(days=14)
    
    dateret2 = dateret1 + timedelta(days=7)
    libelret0 = Capacite.objects.filter(datecapa=dateret0).first().libelle
    libelret1 = Capacite.objects.filter(datecapa=dateret1).first().libelle
    caparet2 = Capacite.objects.filter(datecapa=dateret2).first()
    if caparet2:
        libelret2 = caparet2.libelle
        datechoix = ((dateret0 , libelret0), (dateret1 , libelret1),(dateret2, libelret2))
    else:
        datechoix = ((dateret0 , libelret0),(dateret1 , libelret1))

    form = ModReservationForm(request.POST, initial={'la_date' : datededepot, 'libel_depot' : libeldepot,'choix_date' : datechoix,'la_resa' : resam, 'par_admin' : True})

    if form.is_valid():
        nbreinedemand = form.cleaned_data['nbreine']
        dated = datededepot             
        datert = datetime.datetime.strptime(form.cleaned_data['dateretrait'], "%Y-%m-%d").date()
        # vérification des capacités
        resaok = True
        # Pas de vérificattion, car c'est admin qui fait
        #while (dated < datert):
        #    capac = Capacite.objects.filter(datecapa = dated).first()
        #    if (capac.get_reinesdispos() < nbreinedemand - nbreineavant):
        #        resaok = False
        #        msg += 'Manque de capacité à la station le ' + dated.strftime("%d/%m/%Y")
        #    dated = dated + timedelta(days=7)
        #    print(dated)
        #if nbreinedemand > request.user.nbreinesmax:
        #    resaok = False
        #    msg += 'Vous dépassez votre quotat de ' + str(request.user.nbreinesmax) + ' reines' 
        nbtypfecond1 = form.cleaned_data['nbtypfecond1']
        nbtypfecond2 = form.cleaned_data['nbtypfecond2']
        nbtypfecond3 = form.cleaned_data['nbtypfecond3']
        nbtypfecond4 = form.cleaned_data['nbtypfecond4']
        if (nbtypfecond1 + nbtypfecond2 + nbtypfecond3 + nbtypfecond4) > nbreinedemand:
            resaok = False
            msg += 'Le nombre de ruches est supérieur à celui des reines !  '   
            
        if (resaok):
            #reservation = Reservation()
            resam.apiculteur = api
            resam.nbreine = form.cleaned_data['nbreine']
            resam.datedepot = datededepot 
            resam.dateretrait = form.cleaned_data['dateretrait']
            resam.nbtypfecond1 = form.cleaned_data['nbtypfecond1']
            resam.nbtypfecond2 = form.cleaned_data['nbtypfecond2']
            resam.nbtypfecond3 = form.cleaned_data['nbtypfecond3']
            resam.nbtypfecond4 = form.cleaned_data['nbtypfecond4']
            resam.nbdepotfecond1 = resam.nbtypfecond1
            resam.nbdepotfecond2 = resam.nbtypfecond2
            resam.nbdepotfecond3 = resam.nbtypfecond3
            resam.nbdepotfecond4 = resam.nbtypfecond4
            resam.nbreinedepot = resam.nbreine                                                
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
                
            #  Envoi mail
            subject = 'SFANM - Confirmation modification de réservation'
            html_message = render_to_string('resasfanm/mailconfirmationreservation.html', {'la_resa': resam, 'le_api': resam.apiculteur})
            #plain_message = strip_tags(html_message)
            from_email = 'SFANM <' + settings.DEFAULT_FROM_EMAIL + '>'
            to = api.email
            pdf = Etiquette(resam.id)
            try:
                        #mail.send_mail(subject, html_message, from_email, [to])
                message = EmailMessage(subject=subject,body=html_message,from_email=from_email,to=[to, 'contact@sfanm.fr'])
                message.attach('etiquettes.pdf', pdf, 'application/pdf')

            except Exception as e: print(e)
            else:
                print ('message préparé')
            #message.content_subtype = "text/plain"
                try:
                    message.send() 
                    print('mail envoyé')
                except:
                    print('pb envoi')
                
            return redirect('listentrees', datededepot)  
    else:
        form = ModReservationForm(initial={'la_date' : datededepot, 'libel_depot' : libeldepot,'choix_date' : datechoix,'la_resa' : resam, 'par_admin' : True})
    return render(request, 'resasfanm/newresaapi.html', {'form': form, 'mod' : True, 'msg' : msg, 'le_api' : api, 'date_depot' : datededepot})




# Modification rerservation par un apiculteur
@login_required
def modresa(request,idresa):
    msg =''
    
    resam = Reservation.objects.get(id=idresa)
    print(resam.nbreine)
    nbreineavt = resam.nbreine
    datededepot = resam.datedepot
    capadepot = Capacite.objects.filter(datecapa=datededepot).first()
    libeldepot = capadepot.libelle

# possibilité de ramener 3 reines de plus
    ecartadmis = 0
    datedujour = date.today()
    onestdansles3jours = False
    if (datedujour + timedelta(days=4)) > datededepot:
        ecartadmis = 3
        onestdansles3jours = True

    dateret1 = datededepot + timedelta(days=14)
    caparet1 = Capacite.objects.filter(datecapa=dateret1).first()
    libelret1 = caparet1.libelle    

    # Possibilité de réserver sur 3semaines supprimée
    #dateret2 = dateret1 + timedelta(days=7)
    #caparet2 = Capacite.objects.filter(datecapa=dateret2).first()
    #if caparet2:
    #    libelret2 = caparet2.libelle    
    #    datechoix = ((dateret1 , libelret1),(dateret2, libelret2))
    #else:
    datechoix = ((dateret1 , libelret1),(dateret1 , libelret1))

    form = ModReservationForm(request.POST, initial={'la_date': datededepot, 'libel_depot' : libeldepot, 'choix_date' : datechoix,'la_resa' : resam, 'par_admin' : False})

    if form.is_valid():
        nbreinedemand = form.cleaned_data['nbreine']
        dated = datededepot        

        datert = datetime.datetime.strptime(form.cleaned_data['dateretrait'], "%Y-%m-%d").date()
        # vérification des capacités
        resaok = True
        while (dated < datert):
            capac = Capacite.objects.filter(datecapa = dated).first()
            if (capac.get_reinesdispos() < nbreinedemand - nbreineavt):
                resaok = False
                msg += ' ²Manque de capacité à la station le ' + dated.strftime("%d/%m/%Y")
            dated = dated + timedelta(days=7)
            print(dated)
        if nbreinedemand > (request.user.nbreinesmax + ecartadmis):
            resaok = False
            msg += 'Vous dépassez votre quotat de ' + str(request.user.nbreinesmax + ecartadmis) + ' reines' 
        nbtypfecond1 = form.cleaned_data['nbtypfecond1']
        nbtypfecond2 = form.cleaned_data['nbtypfecond2']
        nbtypfecond3 = form.cleaned_data['nbtypfecond3']
        nbtypfecond4 = form.cleaned_data['nbtypfecond4']
        if (nbtypfecond1 + nbtypfecond2 + nbtypfecond3 + nbtypfecond4) > nbreinedemand:
            resaok = False
            msg += 'Le nombre de ruches est supérieur à celui des reines !  '   
            
        if (resaok):
            #reservation = Reservation()
            resam.apiculteur = request.user
            resam.nbreine = form.cleaned_data['nbreine']
            resam.datedepot = datededepot
    # Possibilité de réserver sur 3semaines supprimée
            resam.dateretrait = dateret1
            #resam.dateretrait = form.cleaned_data['dateretrait']
            resam.nbtypfecond1 = form.cleaned_data['nbtypfecond1']
            resam.nbtypfecond2 = form.cleaned_data['nbtypfecond2']
            resam.nbtypfecond3 = form.cleaned_data['nbtypfecond3']
            resam.nbtypfecond4 = form.cleaned_data['nbtypfecond4']
            resam.nbdepotfecond1 = resam.nbtypfecond1
            resam.nbdepotfecond2 = resam.nbtypfecond2
            resam.nbdepotfecond3 = resam.nbtypfecond3
            resam.nbdepotfecond4 = resam.nbtypfecond4
            resam.nbreinedepot = resam.nbreine                                                
            dated = datededepot             
            #
            resam.save()

    # Possibilité de réserver sur 3semaines supprimée
            dater = dateret1
            #dater = datetime.datetime.strptime(resam.dateretrait, "%Y-%m-%d").date()
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
                
            #  Envoi mail
            subject = 'SFANM - Confirmation modification de réservation'
            html_message = render_to_string('resasfanm/mailconfirmationreservation.html', {'la_resa': resam, 'le_api': resam.apiculteur})
            #plain_message = strip_tags(html_message)
            from_email = 'SFANM <' + settings.DEFAULT_FROM_EMAIL + '>'
            to = request.user.email
            pdf = Etiquette(resam.id)
            try:
                        #mail.send_mail(subject, html_message, from_email, [to])
                message = EmailMessage(subject=subject,body=html_message,from_email=from_email,to=[to])
                message.attach('etiquettes.pdf', pdf, 'application/pdf')

            except Exception as e: print(e)
            else:
                print ('message préparé')
            #message.content_subtype = "text/plain"
                try:
                    message.send() 
                    print('mail envoyé')
                except:
                    print('pb envoi')
                
            return redirect('listresas')  
    else:
        form = ModReservationForm(initial={'la_date': datededepot, 'libel_depot' : libeldepot, 'choix_date' : datechoix,'la_resa' : resam, 'par_admin' : False})
    return render(request, 'resasfanm/newresa.html', {'form': form, 'mod' : True, 'msg' : msg})

@login_required 
def affpourdelresa(request,idresa):
    resam = Reservation.objects.get(id=idresa)
    return render(request, 'resasfanm/affpourdelresa.html', {'la_resa': resam})
    
@login_required 
def affpourdelresaapi(request,idresa):
    resam = Reservation.objects.get(id=idresa)
    return render(request, 'resasfanm/affpourdelresaapi.html', {'la_resa': resam})


@login_required 
def delresa(request,idresa):
    resam = Reservation.objects.get(id=idresa)
    subject = 'SFANM - Confirmation d"annulation de réservation'
    html_message = render_to_string('resasfanm/mailconfirmationannulreservation.html', {'la_resa': resam, 'le_api': resam.apiculteur})
    #plain_message = strip_tags(html_message)
    from_email = 'SFANM <' + settings.DEFAULT_FROM_EMAIL + '>'
    to = request.user.email
    #mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)            
    mail.send_mail(subject, html_message, from_email, [to])             
    resam.delete()
    return redirect('listresas')  

@login_required 
def delResaApi(request,idresa):
    resam = Reservation.objects.get(id=idresa)
    subject = 'SFANM - Confirmation d"annulation de réservation'
    html_message = render_to_string('resasfanm/mailconfirmationannulreservation.html', {'la_resa': resam, 'le_api': resam.apiculteur})
    #plain_message = strip_tags(html_message)
    from_email = 'SFANM <'  + settings.DEFAULT_FROM_EMAIL + '>'
    to = resam.apiculteur.email
    #mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)            
    mail.send_mail(subject, html_message, from_email, [to,'contact@sfanm.fr'])             
    resam.delete()
    return redirect('listgestion')  

@login_required 
def listcapacites(request):
# affiche les dates sur lesquelles l'apiculteur n'a pas réservé
    datesreservees = Reservation.objects.filter(apiculteur=request.user).values_list('datedepot',flat = True)
    # days=0 acr résa possible jusque derrière minute
    datestart = date.today() + timedelta(days=0)
    capacites = Capacite.objects.filter(depotpossible=True).filter(datecapa__gt = datestart).exclude(datecapa__in=datesreservees)
    return render(request, 'resasfanm/capacites.html', {'les_capacites':capacites})


def listouv(request):
#  affiche les dates d'ouverture de la station (pas besoin d'authentification
    if request.user.is_authenticated:
        return redirect('listresas')

    capacites = Capacite.objects.filter(depotpossible=True).filter(datecapa__gt = date.today())
    return render(request, 'resasfanm/listouv.html', {'les_capacites':capacites})

    
    
def listresas(request):
#  affiche les réservations de l'apiculteur et les évènements
    if not request.user.is_authenticated:
        doujeviens = 'listresas'
        return redirect('loginm',doujeviens)
    
    resas = Reservation.objects.filter(apiculteur=request.user).order_by('datedepot')

        
    return render(request, 'resasfanm/listresas.html', {'les_resas':resas})

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
def entreereelle(request,idresa):
    resam = Reservation.objects.get(id=idresa)
    msg = ''
    if request.method == 'POST':
        form = ModEntreeReelleForm(request.POST, initial={'la_resa' : resam, })
        if "cancel" in request.POST:
            return redirect('listentrees', resam.datedepot) 
        else:
            if form.is_valid():
                resam.nbreinedepot = form.cleaned_data['nbreinedepot']
                resam.nbdepotfecond1 = form.cleaned_data['nbdepotfecond1']
                resam.nbdepotfecond2 = form.cleaned_data['nbdepotfecond2']
                resam.nbdepotfecond3 = form.cleaned_data['nbdepotfecond3']
                resam.nbdepotfecond4 = form.cleaned_data['nbdepotfecond4']
                resam.save()
                return redirect('listentrees', resam.datedepot)  # TODO: redirect to the created topic page
            else:
                msg = 'il y a un pb'
    else:
        form = ModEntreeReelleForm(initial={'la_resa' : resam, })

    return render(request, 'resasfanm/entreereelle.html', {'form': form, 'mod' : True, 'msg' : msg, 'la_resa' : resam})

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
    doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(A4), leftMargin=15*mm,topMargin=10*mm, bottomMargin=1*mm)   
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
    data = [['Apicuteur','Prénom','téléphone','Nb reines', 'Apidéa', 'Miniplus', 'Warre', 'Ruchette', 'Total','Emargement']]
# Assemble data for each column using simple loop to append it into data list
    nb1 = 0
    nb2 = 0
    nb3 = 0
    nb4 = 0
    nbr = 0

    for resa in resas:
        if resa.nbreinedepot > 0:
            data.append([resa.apiculteur.nom,resa.apiculteur.prenom, resa.apiculteur.telephone,resa.nbreinedepot, \
                str(resa.nbdepotfecond1) ,resa.nbdepotfecond2, resa.nbdepotfecond3, resa.nbdepotfecond4, resa.nbruchesdepot,''])
            nb1 += resa.nbdepotfecond1
            nb2 += resa.nbdepotfecond2
            nb3 += resa.nbdepotfecond3
            nb4 += resa.nbdepotfecond4                        
            nbr += resa.nbreinedepot                        
    data.append(['','', 'Total', str(nbr), str(nb1), str(nb2), str(nb3), str(nb4), '', '']) \
# nom prenom telephone nb reines nb ruches présent
    tableThatSplitsOverPages = Table(data, colWidths=(45*mm,40*mm,30*mm,20*mm,20*mm, 20*mm, 20*mm, 20*mm, \
         20*mm, 35*mm),rowHeights=(10*mm), repeatRows=1)
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
    data = [['Apicuteur','Prénom','téléphone','Nb reines', 'Apidéa', 'Miniplus', 'Warre', 'Ruchette', 'Total','Emargement']]
# Assemble data for each column using simple loop to append it into data list
    nb1 = 0
    nb2 = 0
    nb3 = 0
    nb4 = 0
    nbr = 0
    for resa in resas:
        if resa.nbreinedepot > 0:
            data.append([resa.apiculteur.nom,resa.apiculteur.prenom, resa.apiculteur.telephone,resa.nbreinedepot, \
                str(resa.nbdepotfecond1) ,resa.nbdepotfecond2, resa.nbdepotfecond3, resa.nbdepotfecond4, resa.nbruchesdepot,''])
            nb1 += resa.nbdepotfecond1
            nb2 += resa.nbdepotfecond2
            nb3 += resa.nbdepotfecond3
            nb4 += resa.nbdepotfecond4                        
            nbr += resa.nbreinedepot                        
    data.append(['','', 'Total', str(nbr), str(nb1), str(nb2), str(nb3), str(nb4), '', '']) \
    # nom prenom telephone nb rei
    # nes nb ruches présent
    tableThatSplitsOverPages = Table(data, colWidths=(45*mm,40*mm,30*mm,20*mm,20*mm, 20*mm, 20*mm, 20*mm, \
         20*mm, 35*mm),rowHeights=(10*mm), repeatRows=1)
    tableThatSplitsOverPages.hAlign = 'LEFT'
    tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LINEBELOW',(0,0),(-1,-1),1,colors.black),
        ('GRID',(0,0),(-1,-1),1,colors.black)])
    tableThatSplitsOverPages.setStyle(tblStyle)
    Story.append(tableThatSplitsOverPages)
        
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


    pdf_buffer.seek(0)
#   return FileResponse(pdf_buffer, as_attachment=True, filename='hello.pdf')
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
    evts = Evenement.objects.filter(date__gt = date.today()).order_by('date')
    return render(request, 'resasfanm/listevenements.html', {'les_evts':evts})

def listevtsmembre(request):
    if not request.user.is_authenticated:
        doujeviens = 'listevtsmembre'
        return redirect('loginm',doujeviens)
    evts = Evenement.objects.filter(date__gte = date.today()).order_by('date')
    for evt in evts:
        if Inscription.objects.filter(evenement=evt,apiculteur=request.user).exists():
            evt.estinscrit=True
        else:
            evt.estinscrit=False
    
    return render(request, 'resasfanm/listevtsmembre.html', {'les_evts':evts})

def listevts(request):
    if request.user.is_authenticated:
        return redirect('listevtsmembre')
    evts = Evenement.objects.filter(date__gte = date.today()).order_by('date')
    
    return render(request, 'resasfanm/listevts.html', {'les_evts':evts})

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
            #       capac = Capacite.objects.filter(datecapa = dated).first()
            #       if (capac.get_reinesdispos() < nbreinedemand):
            #           resaok = False
            #           msg += 'Manque de capacité à la station le ' + dated.strftime("%d/%m/%Y")
            #       dated = dated + timedelta(days=7)
                inscriok = True
                if (inscriok):
                    inscription = Inscription()
                    inscription.apiculteur = request.user
                    api = request.user
                    inscription.evenement = evt
                    inscription.save()
                    subject = 'SFANM - Confirmation d"inscription'
                    html_message = render_to_string('resasfanm/mailconfirmationinscription.html', {'le_evt': evt, 'le_api': api})
                    #plain_message = strip_tags(html_message)
                    from_email = 'SFANM <' + settings.DEFAULT_FROM_EMAIL + '>'
                    to = request.user.email
                    #mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)            
                    mail.send_mail(subject, html_message, from_email, [to])             

                    return redirect('listevtsmembre')  # TODO: redirect to the created topic page
    else:
        form = NewInscriptionForm()
    return render(request, 'resasfanm/new_inscription.html', {'form': form, 'mod' : False, 'msg' : msg, 'le_evt' : evt})

@login_required 
def affpourdelinscription(request,idevt):
    evt = Evenement.objects.get(id=idevt)
    return render(request, 'resasfanm/affpourdelinscrit.html', {'le_evt': evt})

@login_required     
def delinscription(request,idevt):
    evt = Evenement.objects.get(id=idevt)
    inscript = Inscription.objects.get(evenement=idevt,apiculteur=request.user.id)
    subject = 'SFANM - Confirmation d"annulation d"inscription'
    html_message = render_to_string('resasfanm/mailconfirmationannulinscription.html', {'le_evt' : evt})
    #plain_message = strip_tags(html_message)
    from_email = 'SFANM <' + settings.DEFAULT_FROM_EMAIL + '>'
    to = request.user.email
    #mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)            
    mail.send_mail(subject, html_message, from_email, [to])             
    inscript.delete()
    return redirect('listevtsmembre')  

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
    
def Etiquette(idresa):
    PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
    styles = getSampleStyleSheet()

    def myFirstPage(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Bold',16)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-40, Title)
        canvas.setFont('Times-Roman',9)
        canvas.drawString(inch, 0.25 * inch, " %s" % pageinfo)
        canvas.restoreState()

    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman',9)
        canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))
        canvas.restoreState()

    resa = Reservation.objects.get(id=idresa)
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, leftMargin=15*mm,topMargin=10*mm, bottomMargin=1*mm)   
    #doc = SimpleDocTemplate("/tmp/somefilename.pdf", pagesize=A4, topMargin=5*mm, bottomMargin=1*mm)
    Story = []
    style = styles["Normal"]
    Title = "Etiquettes à coller sur vos ruchettes" 
    pageinfo = "Etiquettes SFANM (c)"

    Story.append(Spacer(1, 10*mm))
    
    ptext = '<para align="center" size="16">%s <br/><br/> %s <br/><br/> %s<br/> <br/> <font size="12">Déposé le %s <br/>Retrait le %s</font></para>' \
      % ( resa.apiculteur.nom,resa.apiculteur.prenom, resa.apiculteur.telephone, resa.datedepot.strftime("%d / %m / %y" ), resa.dateretrait.strftime("%d / %m / %y" ))
    print (ptext)
    parag = Paragraph(ptext, styles["Normal"])
    img = Image(os.path.join(settings.STATIC_ROOTDOC, 'img/sfanmlogo.jpg'),width=28*mm,height=28*mm)
    data = []
    for i in range (1,6):
        data.append([img,parag,img,parag])

    tableThatSplitsOverPages = Table(data, colWidths=(30*mm,60*mm,30*mm,60*mm),rowHeights=(50*mm), repeatRows=5)
    tableThatSplitsOverPages.hAlign = 'CENTER'
    tableThatSplitsOverPages.vAlign = 'CENTER'
    tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
        ('VALIGN',(0,0),(-1,-1),'CENTER'),
        ('LINEBELOW',(0,0),(-1,-1),1,colors.black),
        ('BOX',(0,0),(-1,-1),1,colors.black),
        ('BOX',(0,0),(-3,-1),1,colors.black)])

    tableThatSplitsOverPages.setStyle(tblStyle)
    Story.append(tableThatSplitsOverPages)
    
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


    pdf_buffer.seek(0)
#   return FileResponse(pdf_buffer, as_attachment=True, filename='hello.pdf')
    pdf = pdf_buffer.getvalue()
    pdf_buffer.close()
    return pdf
