from django.shortcuts import render
from django.http import HttpResponse

from privateApp import database_fetcher
from .models import Match
# Create your views here.
def home(request):
    

    return HttpResponse('Hello, Django!')