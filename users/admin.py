from django.contrib import admin

# Register your models here.
# src/users/admin.py
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# pour import / export
from .models import CustomUser

class CustomUserResource(resources.ModelResource):
    
    class Meta:
        model = CustomUser

class CustomUserAdminExpImp(ImportExportModelAdmin):
    resource_class = CustomUserResource


#class CustomUserAdmin(UserAdmin):
class CustomUserAdmin(ImportExportModelAdmin):
    model = CustomUser
# pour import / export
    resource_class = CustomUserResource

    list_display = ('email', 'nom', 'prenom','adresse1','adresse2','codepostal','ville','telephone','nbreinesmax','is_staff', 'is_active','acquitte',)
    list_filter = ('email', 'is_staff', 'is_active','acquitte',)
    fieldsets = (
        (None, {'fields': ('email','password', 'nom','prenom','nbreinesmax')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser','acquitte')}),
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
admin.site.register(CustomUser, CustomUserAdmin )

