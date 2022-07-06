# from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class HomeView(TemplateView):
    template_name = 'home/index.html'


class LegalView(TemplateView):
    template_name = "home/legal.html"
