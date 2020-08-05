# views de account
from django.contrib.auth import login as auth_login, authenticate, logout

from django.views.generic.edit import FormView

from django.template.loader import render_to_string

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

from django.middleware.csrf import rotate_token

from django.contrib import messages
from django.core.files.storage import FileSystemStorage, default_storage


from django.shortcuts import render, redirect

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
import csv

from users.models import CustomUser

from .forms import SignUpForm, ContactForm, Okpourcontinuer, SignupForm, LoginForm, MonCompteForm

def signup(request):
    if request.method == 'GET':
        form = SignupForm()
    else:
        form = SignupForm(request.POST)
        if "cancel" in request.POST:
            return redirect('login')
        else:
            if form.is_valid():
                emails = form.cleaned_data['email']
                if CustomUser.objects.filter(email=emails).exists(): # return True/False
                    messages.add_message(request, messages.ERROR, 'le compte existe. Identifiez-vous ou utliser le formulaire de contact')
                else:
                    custuser = CustomUser()
                    custuser.email = emails
                    custuser.nom = form.cleaned_data['nom']
                    custuser.prenom = form.cleaned_data['prenom']
                    custuser.adresse1 = form.cleaned_data['adresse1']
                    custuser.adresse2 = form.cleaned_data['adresse2']
                    custuser.codepostal = form.cleaned_data['codepostal']
                    custuser.ville = form.cleaned_data['ville']
                    custuser.telephone = form.cleaned_data['telephone']
                    custuser.is_active = False
                    custuser.save()
                    html_message = render_to_string('users/signup_email.html', {'le_user': custuser})
                    try:
                        send_mail('[SFANM] : demande adhésion', html_message, 'contact@sfanm.fr', ['contact@sfanm.fr',emails])
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect('users/contactsuccess')
    return render(request, "users/signup.html", {'form': form})

def contactView(request):
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
            return redirect('users/contactsuccess')
    return render(request, "users/contact_email.html", {'form': form})

def successView(request):
    if request.method == 'GET':
        form = Okpourcontinuer()
    else:
        form = Okpourcontinuer(request.POST)
        if form.is_valid():
            return redirect('home')
    return render(request, "users/Okpourcontinuer.html", {'form': form})

@ensure_csrf_cookie
def loginpage(request):
    #rotate_token(request)
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        
        #email = request.POST['email']
        #password =  request.POST['password']
        #post = User.objects.filter(username=username)
        if form.is_valid():
            username = form.cleaned_data['email']
            print(username)
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            print('user')
            print(user)
            print(password)
        #if post:
            #email = request.POST['emai']
            #request.session['email'] = username
            #return redirect("home")
            if user is not None:
                print('on y pass')
                auth_login(request, user)
                if user.is_staff:
                    print('staff')
                    return redirect('home')
                    #return HttpResponseRedirect(reverse_lazy('home')) 
                else:
                #return redirect('listresas') 
                    return HttpResponseRedirect(reverse_lazy('listresas')) 
            #return HttpResponseRedirect(self.success_url)
            
            else:
                messages.add_message(request, messages.INFO, 'Informations de connexion erronées')
                return render(request, 'users/login.html', {'form': form})
    return render(request, 'users/login.html', {'form': form})
 
 
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

    if request.method == 'POST':
        form = MonCompteForm(request.POST, initial={'le_user' : custuser})
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

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        filepath = fs.location + '/' + myfile.name
        with open(filepath, encoding='latin-1') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                custuser = CustomUser()
                custuser.email = row[0]
                custuser.nom = row[1]

                custuser.prenom = row[2]
                custuser.adresse1 = row[3]
                custuser.adresse2 = row[4]
                custuser.codepostal = row[5]
                custuser.ville = row[6]
                custuser.is_active = True
                custuser.save()
                '''try:
                    custuser.save()
                except:
                    print ('probleme svg')'''
        f.close()
                    
        return render(request, 'users/simple_upload.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'users/simple_upload.html')
