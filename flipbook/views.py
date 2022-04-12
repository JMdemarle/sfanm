# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.template import RequestContext
from flipbook.models import PdfFlipbook

#@login_required
def flipbook(request):
    if request.user.is_authenticated:
        documents = PdfFlipbook.objects.all()
        print(documents)

        return render(
            request,
            'index.html',
            {'documents': documents}
        )
    else:
        return redirect('loginadmin')
