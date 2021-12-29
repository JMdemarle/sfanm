"""
url de RESFANM
"""
from django.urls import path, re_path
from . import views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', views.home, name='homeresa'),

    path('newresa/<int:idcapa>',views.newresa,name='newresa'),
    path('modresa/<int:idresa>',views.modresa,name='modresa'),
    path('delresa/<int:idresa>',views.delresa,name='delresa'),
    path('affpourdelresa/<int:idresa>',views.affpourdelresa,name='affpourdelresa'), 
    
    path('modResaApi/<int:idresa>/<int:idapi>',views.modResaApi,name='modResaApi'),
    path('delResaApi/<int:idresa>',views.delResaApi,name='delResaApi'),
    path('affpourdelresaapi/<int:idresa>',views.affpourdelresaapi,name='affpourdelresaapi'), 
    path('newresaapi/<int:idcapa>',views.newresaapi,name='newresaapi'),

    path('newevenement',views.newevenement,name='newevenement'),
    path('listevenements',views.listevenements,name='listevenements'),
    path('listevts',views.listevts,name='listevts'), # liste des évênements visible par tous
    path('listouv',views.listouv,name='listouv'), # liste des ouvertures pour tous    

    path('listevtsmembre',views.listevtsmembre,name='listevtsmembre'),
    
    path('modevenement/<idevt>',views.modevenement,name='modevenement'),
    path('listeparticipants/<idevt>',views.listeparticipants,name='listeparticipants'),
    
    path('newinscription/<idevt>',views.newinscription,name='newinscription'),
    path('delinscription/<idevt>',views.delinscription,name='delinscription'),
    path('voirevt/<idevt>',views.voirevt,name='voirevt'),

    path('affpourdelinscription/<idevt>',views.affpourdelinscription,name='affpourdelinscription'),

    path('capacites',views.listcapacites,name='capacites'),
    path('listresas',views.listresas,name='listresas'),
    path('listgestion',views.listgestion,name='listgestion'),
    path('listentrees/<str:dateentree>',views.listentrees,name='listentrees'),
    path('listsorties/<str:datesortie>',views.listsorties,name='listsorties'),
    path('listsorties/<str:datesortie>',views.listsorties,name='listsorties'),
    path('editentreesortie/<str:dateedit>',views.editentreesortie,name='editentreesortie'),
    path('entreereelle/<int:idresa>',views.entreereelle,name='entreereelle'),
    


]
