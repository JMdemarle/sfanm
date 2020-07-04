# views de account
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect

from .forms import SignUpForm, ContactForm, Okpourcontinuer

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

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
                send_mail(subject, message, from_email, ['jm.demarle@outlook.fr'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('accounts/contactsuccess')
    return render(request, "accounts/contact_email.html", {'form': form})

def successView(request):
    if request.method == 'GET':
        form = Okpourcontinuer()
    else:
        form = Okpourcontinuer(request.POST)
        if form.is_valid():
            return redirect('home')
    return render(request, "accounts/Okpourcontinuer.html", {'form': form})

