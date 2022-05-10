from .models import Player,Match, todo
from django.db import transaction

def add_to_database(JSONdata):
    
    
    if JSONdata:
        with transaction.atomic():
            match_bulk_list = list()
            player_bulk_list = list()
            count = 0
            for q in JSONdata['data']:
                if not JSONdata['data'][q]==[]:
                    for m in JSONdata['data'][q]:
                        try:
                            if not Match.objects.filter(matchId=m['id']).exists() and not Match(matchId=m['id'],rank = m['rank'], sequenceNum = m['sequenceNum'], end_time = m['endDateTime'], lobby_type = m['lobbyType']) in match_bulk_list:
                        
                                new_match = Match(matchId=m['id'],rank = m['rank'], sequenceNum = m['sequenceNum'], end_time = m['endDateTime'], lobby_type = m['lobbyType'] )
                                match_bulk_list.append(new_match)
                                
                                count+=1
                                
                                for p in m['players']:
                                    
                                    hero = str(p['hero'])
                                    hero = hero.removeprefix("{'name': 'npc_dota_hero_")
                                    hero = hero.removesuffix("'}")
                                    player_bulk_list.append(Player(player_id=p['steamAccountId'], match_id = new_match, victory = p['isVictory'],hero = hero,kills= p['kills'],deaths=p['deaths'],assists=p['assists']))
                        except Exception as e:
                            print("error has occured :"+str(e))
            Match.objects.bulk_create(match_bulk_list)
            Player.objects.bulk_create(player_bulk_list)
            print("Added "+str(count)+" match(es) to the database")
                        
                        
    return

def add_todo_to_database(matchIds):
    for id in matchIds:
        if not todo.objects.filter(match_id=id).exists():
            new_todo = todo(match_id = id)
            new_todo.save()