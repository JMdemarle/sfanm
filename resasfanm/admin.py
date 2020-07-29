from django.contrib import admin

# Register your models here.
from .models import Reservation, Capacite, Presence, Evenement, Inscription, TypEmail

admin.site.register(Reservation)
admin.site.register(Capacite)
admin.site.register(Presence)
admin.site.register(Evenement)
admin.site.register(Inscription)
admin.site.register(TypEmail)
