from django.db import models
from django.utils import timezone
from django.utils.text import Truncator
#from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models.functions import Now, ExtractYear
from django.dispatch import receiver 
from django.conf import settings
from users.models import CustomUser


from decimal import *
import datetime
# Create your models here.
'''
class Apiculteur(models.Model):
	nom = models.CharField(max_length=25, unique = True)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null = True)
	def __str__(self):
		""" 
		Cette méthode que nous définirons dans tous les modèles
		nous permettra de reconnaître facilement les différents objets que 
		nous traiterons plus tard dans l'administration
		"""
		return self.user.username


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
	#print('create_user_profile ------------------------')
	#print(instance.username)
	if created:
		
		Apiculteur.objects.create(user=instance,nom=instance.username)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
	#print('save_user_profile')
	try:
		instance.apiculteur.save()
	except:
		instance.apiculteur.nom = instance.username
		Apiculteur.objects.create(user=instance)

'''
class Reservation(models.Model):
	apiculteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='reservations')
	
	nbreine = models.IntegerField(default = 1, verbose_name="nombre reines")
	datedepot = models.DateField(verbose_name="Date depot")
	dateretrait = models.DateField(verbose_name="Date retrait")
	nbtypfecond1 = models.IntegerField(default = 0, verbose_name="nombre apidea/Kieler ")
	nbtypfecond2 = models.IntegerField(default = 0, verbose_name="nombre Miniplus      ")
	nbtypfecond3 = models.IntegerField(default = 0, verbose_name="nombre Warre         ")
	nbtypfecond4 = models.IntegerField(default = 0, verbose_name="nombre ruchette      ")
	ordre = models.IntegerField(verbose_name="ordre",default=1)
	enattente = models.BooleanField(default = False, verbose_name = 'En attente')
	def __str__(self):
		""" 
		Cette méthode que nous définirons dans tous les modèles
		nous permettra de reconnaître facilement les différents objets que 
		nous traiterons plus tard dans l'administration
		"""
		return self.datedepot.strftime('%d/%m/%Y')
		
	
		
	class Meta:
		unique_together = ('apiculteur', 'datedepot',)
	
	@property
	def nbruches(self):
		return self.nbtypfecond1 + self.nbtypfecond2 + self.nbtypfecond3 + self.nbtypfecond4
	
		
	
	
class Capacite(models.Model):
	datecapa = models.DateField(verbose_name="Date Capacité") 
	nreinesmax = models.IntegerField(default = 0, verbose_name="capacité reines")
	stationouverte = models.BooleanField(default = False)
	depotpossible = models.BooleanField(default = True)
	def __str__(self):
		""" 
		Cette méthode que nous définirons dans tous les modèles
		nous permettra de reconnaître facilement les différents objets que 
		nous traiterons plus tard dans l'administration
		"""
		return self.datecapa.strftime('%d/%m/%Y')

	class Meta:
		ordering = ['datecapa']

		
	def get_reinesdispos(self):
		presences = Presence.objects.filter(capa=self)
		nbreines = self.nreinesmax
		for presence in presences:
			nbreines = nbreines - presence.resa.nbreine
		return nbreines
		
	def get_entreesdate(self):
		reservations = Reservation.objects.filter(datedepot=self.datecapa)
		nbentrees = 0
		for reservation in reservations:
			nbentrees = nbentrees + reservation.nbreine
		return nbentrees
		
	def get_sortiesdate(self):
		reservations = Reservation.objects.filter(dateretrait=self.datecapa)
		nbsorties = 0
		for reservation in reservations:
			nbsorties = nbsorties + reservation.nbreine
		return nbsorties
	
	def get_encoursreines(self):
		presences = Presence.objects.filter(capa=self)
		nbreines = 0
		for presence in presences:
			nbreines = nbreines + presence.resa.nbreine
		return nbreines
	
	def get_encoursruches1(self):
		presences = Presence.objects.filter(capa=self)
		nbruches1 = 0
		for presence in presences:
			nbruches1 = nbruches1 + presence.resa.nbtypfecond1
		return nbruches1

	def get_encoursruches2(self):
		presences = Presence.objects.filter(capa=self)
		nbruches2 = 0
		for presence in presences:
			nbruches2 = nbruches2 + presence.resa.nbtypfecond2
		return nbruches2

	def get_encoursruches3(self):
		presences = Presence.objects.filter(capa=self)
		nbruches3 = 0
		for presence in presences:
			nbruches3 = nbruches3 + presence.resa.nbtypfecond3
		return nbruches3

	def get_encoursruches4(self):
		presences = Presence.objects.filter(capa=self)
		nbruches4 = 0
		for presence in presences:
			nbruches4 = nbruches4 + presence.resa.nbtypfecond4
		return nbruches4


class Presence(models.Model):
	resa = models.ForeignKey('Reservation', on_delete=models.CASCADE,related_name='resas')
	capa = models.ForeignKey('Capacite', on_delete=models.CASCADE,related_name='capas')

class TypEmail(models.Model):
	libellé = models.CharField(max_length=25,null=False,default='.')
	template = models.CharField(max_length=35,null=False,default='.')
	objet = models.CharField(max_length=100,null=False,default='.')
	
	def __str__(self):
		return self.libellé
	
	#medicament = models.ForeignKey('TypMedoc', on_delete=models.CASCADE,related_name='medicament', null = True)
	
	
class Evenement(models.Model):

	LDESTMAIL = [
		('0','Tous les membres'),
		('1','Les membres inscrits'),
		('2','Les membres non inscrits'),
		]

	date = models.DateTimeField(verbose_name="Date evenement")
	adresse1 = models.CharField(max_length=40,null=True,default='.')
	adresse2 = models.CharField(max_length=40,null=True,default='.')
	codepostal = models.IntegerField(default = 0,null=True)
	ville = models.CharField(max_length=35,null=True,default='.')

	
	nombremax = models.IntegerField(default = 0, verbose_name="nombre participants")
	intitule = models.CharField(max_length=100,null=False,default='.')
	programme = models.TextField(verbose_name = 'programme', null = True)
	natmail1 = models.ForeignKey('TypEmail', on_delete=models.CASCADE,related_name='nmail1', null = True)
	
	destmail1 = models.IntegerField(choices=LDESTMAIL,null = True,default=0)
	datemail1 = models.DateField(verbose_name="date mail 1",null=True)
	natmail2 = models.ForeignKey('TypEmail', on_delete=models.CASCADE,related_name='nmail2', null = True)
	destmail2 = models.IntegerField(choices=LDESTMAIL,null = True,default=0)
	datemail2 = models.DateField(verbose_name="date mail 2",null=True)

	class Meta:
		unique_together = ('date', 'intitule',)
		#ordering = ['date']

	def __str__(self):
		return self.date.strftime('%d/%m/%Y') + self.intitule
		
	def get_nbparticipants(self):
		nbpart = Inscription.objects.filter(evenement=self).count()
		return nbpart
		
	def get_placeslibres(self):
		nblibre = self.nombremax - Inscription.objects.filter(evenement=self).count()
		return nblibre		
		

class Inscription(models.Model):
	evenement = models.ForeignKey('Evenement', on_delete=models.CASCADE,related_name='partevts')
	apiculteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='partapis')

	class Meta:
		unique_together = ('evenement', 'apiculteur',)
		
	def __str__(self):
		return self.apiculteur.nom + self.evenement.intitule
		
	
