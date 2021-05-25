# initialisation des depots rréesl
# suite à changement modèle
from django.core.management.base import BaseCommand

from resasfanm.models import Reservation, Capacite, Presence, Evenement, Inscription

class Command(BaseCommand):
    help = 'initialisation champs réservation'

    def handle(self, *args, **kwargs):

        resas = Reservation.objects.all()
        for resa in resas:

            resa.nbdepotfecond1 = resa.nbtypfecond1
            resa.nbdepotfecond2 = resa.nbtypfecond2
            resa.nbdepotfecond3 = resa.nbtypfecond3
            resa.nbdepotfecond4 = resa.nbtypfecond4
            resa.nbreinedepot = resa.nbreine
            resa.save()

