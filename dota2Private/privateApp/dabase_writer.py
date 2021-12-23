from .models import Player,Match, todo

def add_to_database(JSONdata):
    
    if JSONdata:
        
        for m in JSONdata['data']['matches']:
            
            if not Match.objects.filter(matchId=m['id']).exists():
                
                newMatch = Match(matchId=m['id'],rank = m['rank'], sequenceNum = m['sequenceNum'], end_time = m['endDateTime'], lobby_type = m['lobbyType'] )
                newMatch.save()
                print('Wrote match: '+ str(m['id']) +' to database')
                
                for p in m['players']:
                    
                    hero = str(p['hero'])
                    hero = hero.removeprefix("{'name': 'npc_dota_hero_")
                    hero = hero.removesuffix("'}")
                    newPlayer = Player(player_id=p['steamAccountId'], match_id = newMatch, victory = p['isVictory'],hero = hero,kills= p['kills'],deaths=p['deaths'],assists=p['assists'])
                    newPlayer.save()
                        
    return

def add_todo_to_database(matchIds):
    for id in matchIds:
        new_todo = todo(match_id = id)
        new_todo.save()