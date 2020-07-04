from django.contrib import admin

# Register your models here.
from .models import Reservation, Capacite, Presence, Apiculteur

admin.site.register(Reservation)
admin.site.register(Capacite)
admin.site.register(Presence)
admin.site.register(Apiculteur)
