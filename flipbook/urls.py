# -*- coding: utf-8 -*-
from django.urls import re_path
from django.views.generic import TemplateView
from flipbook.views import flipbook

urlpatterns = [
    re_path(r'^$', flipbook, name='flipbook'),
    re_path(r'^viewer.html$', TemplateView.as_view(template_name="viewer.html", content_type="text/html"), name="viewer") # only relevant when using pdfjs-flipbook
]
