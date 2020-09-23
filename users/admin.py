from django.contrib import admin

# Register your models here.
# src/users/admin.py
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


from .models import CustomUser



class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'nom', 'prenom','adresse1','adresse2','codepostal','ville','telephone','nbreinesmax','is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email','password', 'nom','prenom','nbreinesmax')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser')}),
        ('coordonnées',{'fields': ('adresse1','adresse2','codepostal','ville','telephone')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
     )
    search_fields = ('email',)
    ordering = ('email',)


#admin.site.unregister(CustomUser)
admin.site.register(CustomUser, CustomUserAdmin)

