from django.core import mail
from django.core.mail import EmailMessage

from datetime import date, datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.template.loader import render_to_string
#from django.core.files.storage import  default_storage
from django.template.loader import get_template

from resasfanm.models import Reservation, Capacite, Presence, Evenement, Inscription
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Mailings: évènements et réservation'

    def maildepot(self, resa):
        print(resa.apiculteur.nom)
        subject = 'SFANM - Rappel de votre depot du ' + resa.datedepot.strftime('%d-%m-%Y')
        html_message = render_to_string('resasfanm/maildepot.html', {'la_resa': resa})
        from_email = 'SFANM <sfanm@demarle.net>'
        to = resa.apiculteur.email
        mail.send_mail(subject, html_message, from_email, [to])             
        
    def mailretrait(self, resa):
        print(resa.apiculteur.nom)
        subject = 'SFANM - Rappel de votre retrait du ' + resa.dateretrait.strftime('%d-%m-%Y')
        html_message = render_to_string('resasfanm/mailretrait.html', {'la_resa': resa})
        from_email = 'SFANM <sfanm@demarle.net>'
        to = resa.apiculteur.email
        mail.send_mail(subject, html_message, from_email, [to])
        
    def maildest(self, mbr, evt, destin):
            # 0 tous les membres
        AEnvoyer = False
        if (destin == 0):
            AEnvoyer = True
        # 1 les inscrits
        elif (destin == 1):
            if Inscription.objects.filter(evenement=evt,apiculteur=mbr).exists():
                AEnvoyer = True
        # les non inscrits
        elif (destin == 2):
            if not Inscription.objects.filter(evenement=evt,apiculteur=mbr).exists():
                AEnvoyer = True
        return AEnvoyer

            
        
    def mailevtdate(self,evt, natmail, destmail):
        if natmail is not None and destmail is not None:
            templa = 'resasfanm/' + natmail.template
            print (templa)
            try:
                tmp  = get_template(templa)
            except:
                print('non existe')
            else:
                print('existe')
                # boucle sur les membres
                mbrs = CustomUser.objects.filter(is_active = True)
                for mbr in mbrs:
                    if self.maildest(mbr, evt, destmail):
                        subject = natmail.objet + ' - ' + evt.intitule
                        html_message = render_to_string(templa, {'le_evt': evt})
                        print(html_message)
                        from_email = 'SFANM <sfanm@demarle.net>'
                        try:
                        #mail.send_mail(subject, html_message, from_email, [to])
                            message = EmailMessage(subject=subject,body=html_message,from_email=from_email,to=[mbr.email])
                        except Exception as e: print(e)
                        else:
                            print ('message préparé')
                            #message.content_subtype = "text/plain"
                            try:
                                message.send() 
                            except:
                                print('pb envoi')
                        

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)
        datej = date.today()
        datej3 = datej + timedelta(days=3)
        print(datej3)
        
        # mailing de rappel pour les réservations
        resas = Reservation.objects.all()
        for resa in resas:
            print (resa.datedepot)
            print (resa.dateretrait)
            
            if (resa.datedepot == datej3 ):
                self.maildepot(resa)
            if (resa.dateretrait == datej3 ):
                self.mailretrait(resa)
                
        # mailing pour les évênements
        evts = Evenement.objects.all()
        for evt in evts:
            if evt.datemail1 is not None:
                if (evt.datemail1 == datej):
                    self.mailevtdate(evt, evt.natmail1, evt.destmail1)
            if evt.datemail2 is not None:
                if (evt.datemail2 == datej ):
                    self.mailevtdate(evt, evt.natmail2, evt.destmail2)


