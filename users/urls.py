"""
url de USERS
"""
from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views
#from users import views as users_views

urlpatterns = [
    #path('login', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('login', views.loginpage, name='login'),
    
    path('logout', auth_views.LogoutView.as_view(), name='logout'),

    path('mon_compte',views.mon_compte,name='mon_compte'),
    path('cup',views.cup,name='cup'),
    
    path('signup', views.signup, name='signup'),
    path('reset', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html',
        email_template_name='users/password_reset_email.html',
        subject_template_name='users/password_reset_subject.txt'), 
        name='password_reset'),
    path('reset/done',
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('reset/complete',
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),
    path('contact', views.contactView, name='contact'),
    path('users/contactsuccess', views.successView, name='contactsucccess'),

    path('upload',views.simple_upload,name='upload'),
    

    

]
"""
urlpatterns = [
    
    #path('signup', views.signup, name='signup'),
    #path('signup', accounts_views.signup, name='signup'),
    #path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('login', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    #path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login2'),

    path('reset', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt'), 
        name='password_reset'),
    path('reset/done',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('reset/complete',
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),
        
    path('contact', accounts_views.contactView, name='contact'),
    path('accounts/contactsuccess', accounts_views.successView, name='contactsucccess'),
    
]
"""
