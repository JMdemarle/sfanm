# views de account
from django.contrib.auth import login as auth_login, authenticate, logout

from django.views.generic.edit import FormView

from django.template.loader import render_to_string

from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.views import PasswordResetView

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

from django.middleware.csrf import rotate_token
from django.views.decorators.clickjacking import xframe_options_exempt

from django.contrib import messages
from django.core.files.storage import FileSystemStorage, default_storage

from django.shortcuts import render, redirect

from django.core.mail import send_mail, BadHeaderError

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy,resolve, Resolver404
import csv

from users.models import CustomUser

from .forms import SignUpForm, ContactForm, Okpourcontinuer, SignupForm, SignupNewForm, SignupAgainForm, LoginForm, MonCompteForm, ModMembreForm

@staff_member_required
def listmembres(request):
    if not request.user.is_authenticated:
        doujeviens = 'listmembres'
        return redirect('login',doujeviens)
    membres = CustomUser.objects.all().order_by('nom')
    return render(request, 'users/listmembres.html', {'les_membres':membres})

@login_required 
@staff_member_required    
def mailacquit(request,membreid):
    membre = CustomUser.objects.get(id=membreid)
    membre.is_active = True
    membre.acquitte = True
    membre.save()
    subject = 'SFANM - Confirmation d Adhésion'
    html_message = render_to_string('users/mailconfirmationadhesion.html', {'le_user' : membre})
    #plain_message = strip_tags(html_message)
    from_email = 'SFANM <ne-pas-repondre@sfanm.fr>'
    to = membre.email
    #mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)            
    send_mail(subject, html_message, from_email, ['contact@sfanm.fr',to,'jm.demarle@outlook.fr'])   
    return redirect('contactsuccess','/users/listmembres')
    #return redirect('listmembres')  

@login_required 
@staff_member_required
def membresrazacquitte(request):
    membres = CustomUser.objects.all()
    for membre in membres:
        membre.acquitte = False
        membre.is_active = False
        membre.save()
    return redirect('listmembres')

@login_required 
@staff_member_required
def razacquitte(request):
    return render(request, 'users/razacquitte.html')

@login_required 
@staff_member_required
def modmembre(request,membreid):
    membre = CustomUser.objects.get(id=membreid)
    print(membre.nom)
    form = ModMembreForm(request.POST, initial={'le_membre' : membre})
    if request.method == 'POST':
        if "cancel" in request.POST:
            return redirect('listmembres')
        else:
            if form.is_valid():
                print('form is valid')
                membre.is_active = form.cleaned_data['is_active']
                membre.nbreinesmax = form.cleaned_data['nbreinesmax']
                membre.acquitte = form.cleaned_data['acquitte']
                
                membre.save()
                return redirect('listmembres')
    else:
        form = ModMembreForm(initial={'le_membre' : membre})
    return render(request, 'users/modmembre.html', {'form': form,'le_membre': membre})


def signup(request):
   return render(request, 'users/signup.html')

class PasswordResetViewNew(PasswordResetView):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        if CustomUser.objects.filter(email=email).exists():
            if CustomUser.objects.get(email=email).is_active:
                return super(PasswordResetViewNew, self).post(request, *args, **kwargs)
            else:
                messages.add_message(request, messages.ERROR, 'Compte inactif. Les droits ne sont pas ouverts')
        else:
            messages.add_message(request, messages.ERROR, 'Le compte n"existe pas.')
        return render(request, "users/password_reset.html", {'form': PasswordResetForm})
                   


def signupnew(request):
    url = request.GET.get("next")       
    if request.method == 'GET':
        form = SignupNewForm()
    else:
        form = SignupNewForm(request.POST)
        if "cancel" in request.POST:
            try:
                resolve(url)
                return HttpResponseRedirect(url)
            except Resolver404: # Make sure the url comes from your project
                if request.user.is_authenticated:
                    if request.user.is_staff:
                        return redirect('home')
                    else:
                        return redirect('listresas')
                else:
                    return redirect('signup')
        else:
            if form.is_valid():
                emails = form.cleaned_data['email']
                if CustomUser.objects.filter(email=emails).exists(): # return True/False
                    messages.add_message(request, messages.ERROR, 'Le compte existe.')
                    messages.add_message(request, messages.ERROR, 'Est-ce pour un renouvellement d"adhésion?')
                else:
                    custuser = CustomUser()
                    custuser.email = emails
                    custuser.nom = form.cleaned_data['nom'].upper()
                    custuser.prenom = form.cleaned_data['prenom'].title()
                    custuser.adresse1 = form.cleaned_data['adresse1']
                    custuser.adresse2 = form.cleaned_data['adresse2']
                    custuser.codepostal = form.cleaned_data['codepostal']
                    custuser.ville = form.cleaned_data['ville']
                    custuser.telephone = form.cleaned_data['telephone']
                    custuser.is_active = False
                    custuser.save()
                    html_message = render_to_string('users/signup_email.html', {'le_user': custuser, 'le_motif': "d adhésion"})
                    try:
                        send_mail('[SFANM] : demande adhésion', html_message, 'ne-pas-repondre@sfanm.fr', ['contact@sfanm.fr',emails,'jm.demarle@outlook.fr'])
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect('signupsuccess')
    return render(request, "users/signupnew.html", {'form': form})

def signupagain(request):
    url = request.GET.get("next")
    if request.method == 'GET':
        form = SignupAgainForm()
    else:
        form = SignupAgainForm(request.POST)
        if "cancel" in request.POST:
            try:
                resolve(url)
                return HttpResponseRedirect(url)
            except Resolver404: # Make sure the url comes from your project
                if request.user.is_authenticated:
                    if request.user.is_staff:
                        return redirect('home')
                    else:
                        return redirect('listresas')
                else:
                    return redirect('signup')
        else:
            if form.is_valid():
                emails = form.cleaned_data['email']
                if CustomUser.objects.filter(email=emails).exists(): # return True/False
                    custuser = CustomUser.objects.get(email=emails)
                    html_message = render_to_string('users/signup_email.html', {'le_user': custuser, 'le_motif': "de renouvellement d adhésion" })
                    try:
                        send_mail('[SFANM] : demande renouvellement adhésion', html_message, 'ne-pas-repondre@sfanm.fr', ['contact@sfanm.fr',emails,'jm.demarle@outlook.fr'])
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect('signupsuccess')
                    
                else:
                    messages.add_message(request, messages.ERROR, 'Le compte n"existe pas.')
                    messages.add_message(request, messages.ERROR, 'Corrigez votre Email  ou faites une "nouvelle adhésion"')
    return render(request, "users/signupagain.html", {'form': form})

def contactView(request):
    url = request.GET.get("next")
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['contact@sfanm.fr'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
                
            return redirect('contactsuccess',url)
    return render(request, "users/contact_email.html", {'form': form})

def successView(request,url):
    if request.method == 'GET':
        form = Okpourcontinuer()
    else:
        form = Okpourcontinuer(request.POST)
        if form.is_valid():
            try:
                resolve(url)
                return HttpResponseRedirect(url)
            except Resolver404: # Make sure the url comes from your project
                if request.user.is_authenticated:
                    if request.user.is_staff:
                        return redirect('home')
                    else:
                        return redirect('listresas') 
                else:
                    return redirect('signup')
            
            return redirect('home')
    return render(request, "users/Okpourcontinuer.html", {'form': form})

def signupsuccess(request):
   return render(request, 'users/Okstop.html')

@ensure_csrf_cookie
@xframe_options_exempt
def loginpage(request,doujeviens):
    # lgon pour menu réservations et menu formation
    #rotate_token(request)
    #print(doujeviens)
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
        #if post:
            #email = request.POST['emai']
            #request.session['email'] = username
            #return redirect("home")
            if user is not None:
                auth_login(request, user)
                if user.is_staff:
                    return redirect('home')
                    #return HttpResponseRedirect(reverse_lazy('home')) 
                else:
                    return redirect(doujeviens)
                    
                    #"return redirect('listresas') 
                    #return HttpResponseRedirect(reverse_lazy('listresas')) 
            #return HttpResponseRedirect(self.success_url)
            
            else:
                nb = CustomUser.objects.filter(email=username).count()
                if nb > 0:
                    us = CustomUser.objects.filter(email=username)
                    if us[0].acquitte == False:    
                        messages.add_message(request, messages.INFO, 'Accès non encore ouvert')
                    else:
                        messages.add_message(request, messages.INFO, 'Mot de passe erroné')                     
                else:
                    messages.add_message(request, messages.INFO, 'Informations de connexion erronées - email')
                return render(request, 'users/loginevt.html', {'form': form, 'doujeviens': doujeviens})
    return render(request, 'users/loginevt.html', {'form': form, 'doujeviens': doujeviens})

@ensure_csrf_cookie
@xframe_options_exempt
def login(request):
# login pour admin
    #rotate_token(request)
    #print(doujeviens)
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
        #if post:
            #email = request.POST['emai']
            #request.session['email'] = username
            #return redirect("home")
            if user is not None:
                auth_login(request, user)
                if user.is_staff:
                    return redirect('home')
                else:
                    return redirect('listresas') 
            
            else:
                messages.add_message(request, messages.INFO, 'Informations de connexion erronées')
                return render(request, 'users/loginevt.html', {'form': form})
    return render(request, 'users/loginevt.html', {'form': form})

@ensure_csrf_cookie
@xframe_options_exempt
def loginadmin(request):
# login pour admin
    #rotate_token(request)
    #print(doujeviens)
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
        #if post:
            #email = request.POST['emai']
            #request.session['email'] = username
            #return redirect("home")
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            
            else:
                messages.add_message(request, messages.INFO, 'Informations de connexion erronées')
                return render(request, 'users/loginadmin.html', {'form': form})
    return render(request, 'users/loginadmin.html', {'form': form})


def logoutevt(request):
     logout(request)
     return redirect('listevts')
     
def logoutresa(request):
     logout(request)
     return redirect('listouv')     
 
'''class loginpage(FormView):
    """login view"""

    form_class = LoginForm
    success_url = reverse_lazy('home')
    template_name = 'users/login.html'

    def form_valid(self, form):
        """ process user login"""
        credentials = form.cleaned_data

        user = authenticate(username=credentials['email'],
                            password=credentials['password'])

        if user is not None:
            print('on y pass')
            auth_login(self.request, user)
            if user.is_staff:
                print('staff')
                #return redirect('home')
                return HttpResponseRedirect(reverse_lazy('home')) 
            else:
                #return redirect('listresas') 
                return HttpResponseRedirect(reverse_lazy('listresas')) 
            #return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(self.request, messages.INFO, 'Informations de connexion erronées')
            return HttpResponseRedirect(reverse_lazy('login'))    '''


    
'''def profile(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        query = User.objects.filter(username=posts) 
        return render(request, 'app_foldername /profile.html', {"query":query})
    else:
        return render(request, 'app_foldername/login.html', {}) '''

@login_required
def mon_compte(request):
    msg = ''
    custuser = request.user
    url = request.GET.get("next")

    if request.method == 'POST':
        form = MonCompteForm(request.POST, initial={'le_user' : custuser})
        if "cancel" in request.POST:
            try:
                resolve(url)
                return HttpResponseRedirect(url)
            except Resolver404: # Make sure the url comes from your project
                if custuser.is_staff:
                    return redirect('home')
                else:
                    return redirect('listresas') 
        else:
            if form.is_valid():
                custuser.nom = form.cleaned_data['nom'].upper()
                custuser.prenom = form.cleaned_data['prenom'].title()
                custuser.adresse1 = form.cleaned_data['adresse1']
                custuser.adresse2 = form.cleaned_data['adresse2']
                custuser.codepostal = form.cleaned_data['codepostal']
                custuser.ville = form.cleaned_data['ville']
                custuser.telephone = form.cleaned_data['telephone']
                custuser.save()
                try:
                    resolve(url)
                    return HttpResponseRedirect(url)
                except Resolver404: # Make sure the url comes from your project
                
                    if custuser.is_staff:
                        return redirect('home')
                    else:
                        return redirect('listresas') 
    else:
        form = MonCompteForm(initial={'le_user' : custuser})
    return render(request, 'users/moncompte.html', {'form': form, 'mod' : True, 'msg' : msg})
    

@login_required
def cup(request):
    msg = ''

    if request.method == 'POST':
        form = CupForm(request.POST)
        if "cancel" in request.POST:
            if custuser.is_staff:
                return redirect('home')
            else:
                return redirect('listresas') 
        else:
            if form.is_valid():
                
                custuser.nom = form.cleaned_data['nom']
                custuser.prenom = form.cleaned_data['prenom']
                custuser.adresse1 = form.cleaned_data['adresse1']
                custuser.adresse2 = form.cleaned_data['adresse2']
                custuser.codepostal = form.cleaned_data['codepostal']
                custuser.ville = form.cleaned_data['ville']
                custuser.telephone = form.cleaned_data['telephone']
                custuser.save()
                if custuser.is_staff:
                    return redirect('home')
                else:
                    return redirect('listresas') 
    else:
        form = MonCompteForm(initial={'le_user' : custuser})
    return render(request, 'users/moncompte.html', {'form': form, 'mod' : True, 'msg' : msg})

# Chargement de la liste des adhérents
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        filepath = fs.location + '/' + myfile.name
        # encod latin-1
        with open(filepath, encoding='utf') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                custuser = CustomUser()
                custuser.email = row[3]
                custuser.nom = row[1]

                custuser.prenom = row[2]
                custuser.adresse1 = row[4]
                custuser.adresse2 = ''
                custuser.codepostal = row[5]
                custuser.ville = row[6]
                custuser.telephone =row[8]
                custuser.is_active = True
                custuser.acquitte = True
                custuser.save()
                '''try:
                    custuser.save()
                except:
                    print ('probleme svg')'''
        f.close()
                    
        return render(request, 'users/simple_upload.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'users/simple_upload.html')
