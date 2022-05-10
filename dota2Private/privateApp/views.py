from django.shortcuts import render
from django.http import HttpResponse

from privateApp import database_fetcher
from .models import Match, Player
import time
# Create your views here.
def home(request):
    
    matches = Match.objects.all()
    

    return render(request, "privateApp/home.html")

def search(request):
    query = request.GET.get('search')
    player_result = Player.objects.all()
    if query:
        player_result = Player.objects.filter(player_id =query)
    
    match_result= Match.objects.all()
    if query:
        match_result=Match.objects.filter(matchId=query)
    context ={'result': player_result,'match_result':match_result}
    
    

    return render(request, "privateApp/results.html",context)