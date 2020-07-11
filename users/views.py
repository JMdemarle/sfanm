# views de account
from django.contrib.auth import login as auth_login, authenticate, logout

from django.views.generic.edit import FormView

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.shortcuts import render, redirect

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy


from .forms import SignUpForm, ContactForm, Okpourcontinuer, SignupForm, LoginForm

def signup(request):
    if request.method == 'GET':
        form = SignupForm()
    else:
        form = SignupForm(request.POST)
        if form.is_valid():
            from_email = form.cleaned_data['from_email']
            try:
                send_mail('demande adhésion', from_email, from_email, ['contact@sfnam.fr'])
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
                send_mail(subject, message, from_email, ['contact@sfnam.fr'])
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
'''
def loginpage(request):
    if request.method == 'POST':
        email = request.POST['email']
        password =  request.POST['password']
        post = User.objects.filter(username=username)
        if post:
            email = request.POST['emai']
            request.session['email'] = username
            return redirect("home")
        else:
            return render(request, 'users/login.html', {})
    return render(request, 'users/login.html', {})
 '''   
class loginpage(FormView):
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
            auth_login(self.request, user)
            if user.is_staff:
                return redirect('home')
            else:
                return redirect('listresas') 
            #return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(self.request, messages.INFO, 'Informations de connexion erronées')
            return HttpResponseRedirect(reverse_lazy('login'))    
    
def profile(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        query = User.objects.filter(username=posts) 
        return render(request, 'app_foldername /profile.html', {"query":query})
    else:
        return render(request, 'app_foldername/login.html', {})

