"""
url de ruchers
"""
from django.urls import path, re_path
from . import views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', views.listresas, name='homeresa'),

    path('newresa/<int:idcapa>',views.newresa,name='newresa'),
    path('modresa/<int:idresa>',views.modresa,name='modresa'),
    path('affpourdelresa/<int:idresa>',views.affpourdelresa,name='affpourdelresa'),    


    path('capacites',views.listcapacites,name='capacites'),
    path('listresas',views.listresas,name='listresas'),
    path('listgestion',views.listgestion,name='listgestion'),
    path('listentrees/<str:dateentree>',views.listentrees,name='listentrees'),
    path('listsorties/<str:datesortie>',views.listsorties,name='listsorties'),
    


]
