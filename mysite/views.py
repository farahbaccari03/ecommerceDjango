from django.shortcuts import render 
from django.template import loader
from . import templates 


def index (request):
    return render(request, 'acceuil.html')