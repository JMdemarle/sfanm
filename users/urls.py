"""
url de USERS
"""
from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.conf import settings


#from users import views as users_views

urlpatterns = [
    #path('login', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('loginm/<str:doujeviens>', views.loginpage, name='loginm'),
    path('login', views.login, name='login'),
    path('loginadmin', views.loginadmin, name='loginadmin'),
    
    
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('logoutevt', views.logoutevt, name='logoutevt'),
    path('logoutresa', views.logoutresa, name='logoutresa'),

    path('listmembres',views.listmembres,name='listmembres'),   
    path('mailacquit/<int:membreid>',views.mailacquit,name='mailacquit'),
    path('membresrazacquitte',views.membresrazacquitte,name='membresrazacquitte'),
    path('razacquitte',views.razacquitte,name='razacquitte'),
    
    path('modmembre/<int:membreid>',views.modmembre,name='modmembre'),
    path('creemembre',views.creemembre,name='creemembre'),    


    path('mon_compte',views.mon_compte,name='mon_compte'),
    
    path('cup',views.cup,name='cup'),
    
    path('signup', views.signup, name='signup'),
    path('signupnew', views.signupnew, name='signupnew'),
    path('signupagain', views.signupagain, name='signupagain'),
    
#    path('reset', auth_views.PasswordResetView.as_view(
    path('reset', views.PasswordResetViewNew.as_view(
        template_name='users/password_reset.html',
        email_template_name='users/password_reset_email.html',
        subject_template_name='users/password_reset_subject.txt',
        from_email='SFANM <' + settings.DEFAULT_FROM_EMAIL + '>'), 
        name='password_reset'),
        
        
    path('resetevt', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset_evt.html',
        email_template_name='users/password_reset_email.html',
        subject_template_name='users/password_reset_subject.txt',
        from_email='SFANM <' + settings.DEFAULT_FROM_EMAIL + '>',
        success_url = reverse_lazy('password_reset_done_evt')), 
        name='password_reset_evt'),
    path('resetevt/done',
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done_evt.html'),
        name='password_reset_done_evt'),
    path('resetresa', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset_resa.html',
        email_template_name='users/password_reset_email.html',
        subject_template_name='users/password_reset_subject.txt',
        from_email='SFANM <' + settings.DEFAULT_FROM_EMAIL + '>',
        success_url = reverse_lazy('password_reset_done_resa')), 
        name='password_reset_resa'),
    path('resetresa/done',
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done_resa.html'),
        name='password_reset_done_resa'),
     path('reset/done',
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'),       
        
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('reset/complete',
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),
    path('contact', views.contactView, name='contact'),
    path('contactsuccess<path:url>', views.successView, name='contactsuccess'),
    path('signupsuccess', views.signupsuccess, name='signupsuccess'),

    path('upload',views.simple_upload,name='upload'),
        
]
    

