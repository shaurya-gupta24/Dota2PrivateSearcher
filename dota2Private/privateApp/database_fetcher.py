import requests
import json
from .dabase_writer import add_to_database, add_todo_to_database

def get_games(id):
    #first sequence = 5263928311
    #id = str(5263928429)
    response = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistoryBySequenceNum/V001/?start_at_match_seq_num="+id+"&key=CFEDF7BDE890FF457BA7A4496899AEC0&matches_requested=10")
    #response = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key=CFEDF7BDE890FF457BA7A4496899AEC0")
    print(response.status_code)
    if(response.status_code == 200):
        data = response.json()
        matchIds=[]
        for e in data['result']['matches']:
            matchIds.append(e['match_id'])
        print(matchIds)
        accessToken = ""
        header = {"Authorization": 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiJodHRwczovL3N0ZWFtY29tbXVuaXR5LmNvbS9vcGVuaWQvaWQvNzY1NjExOTgwNDY5MDg4NjkiLCJ1bmlxdWVfbmFtZSI6Im5pZ2VsIiwiU3ViamVjdCI6ImViYjVmNGY0LTU4NTgtNDdhZS05MWM3LTI4OWY1ZGI1MWI1OSIsIlN0ZWFtSWQiOiI4NjY0MzE0MSIsIm5iZiI6MTYyNTk2ODY1MiwiZXhwIjoxNjU3NTA0NjUyLCJpYXQiOjE2MjU5Njg2NTIsImlzcyI6Imh0dHBzOi8vYXBpLnN0cmF0ei5jb20ifQ.toXm-2QzJagGjMs2_c6m7L61u0YQlEF0uk-7GPDWUGs'}
        url = 'https://api.stratz.com/graphql'
        query = """query getMatches($id: [Long]!){
            matches(ids: $id ){
  	            id
                rank
                sequenceNum
                lobbyType
                endDateTime
                regionId
                players{
                    steamAccountId
                    isVictory
                    hero{
                    name
                    }
                    kills
                    deaths
                    assists 
                }
            }
        }
            """
        variables= {'id': matchIds}
        r = requests.post(url,json={"query": query, 'variables': variables}, headers = header)
        print(r.status_code)
        if(r.status_code == 200):
            data = r.json()
            success = add_to_database(data)
            lastid = data['data']['matches'][0]['sequenceNum']
            if str(lastid) == id:
                lastid = data['data']['matches'][(len(data['data']['matches'])-1)]['sequenceNum']
            print(lastid)
            
        else:
            success = False
    lastid = str(lastid)
    with open('dota2Private\privateApp\lastSequence.txt', "w") as myfile:
        myfile.write(lastid)
    return success, lastid
        

    


def getGamesDota2Api(id, matchIds):
    #first sequence = 5263928311
    #id = str(5263928429)
    response = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistoryBySequenceNum/V001/?start_at_match_seq_num="+id+"&key=CFEDF7BDE890FF457BA7A4496899AEC0&matches_requested=100")
    #response = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key=CFEDF7BDE890FF457BA7A4496899AEC0")
    print(response.status_code)
    if(response.status_code == 200):
        data = response.json()
        acceptable_ids=[121,122,123,124,131,132,133,134,135,136,137,138,181,182,183,184,185,186,187,188,191,192,193]
        
        for e in data['result']['matches']:
            if e['cluster'] in acceptable_ids:
                matchIds.append(e['match_id'])
    
    return response.status_code, matchIds


def getmatchesDetailsStratz(matchIds,oldId):
    data = {}
    print(matchIds)
    key1 = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiJodHRwczovL3N0ZWFtY29tbXVuaXR5LmNvbS9vcGVuaWQvaWQvNzY1NjExOTgwNDY5MDg4NjkiLCJ1bmlxdWVfbmFtZSI6Im5pZ2VsIiwiU3ViamVjdCI6ImViYjVmNGY0LTU4NTgtNDdhZS05MWM3LTI4OWY1ZGI1MWI1OSIsIlN0ZWFtSWQiOiI4NjY0MzE0MSIsIm5iZiI6MTYyNTk2ODY1MiwiZXhwIjoxNjU3NTA0NjUyLCJpYXQiOjE2MjU5Njg2NTIsImlzcyI6Imh0dHBzOi8vYXBpLnN0cmF0ei5jb20ifQ.toXm-2QzJagGjMs2_c6m7L61u0YQlEF0uk-7GPDWUGs'
    key2 = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiJodHRwczovL3N0ZWFtY29tbXVuaXR5LmNvbS9vcGVuaWQvaWQvNzY1NjExOTg4NzEzNTQ0OTciLCJ1bmlxdWVfbmFtZSI6InByYWduYW50IHNvbmljIDopIiwiU3ViamVjdCI6IjQ4MTM4NGFkLTM4MjEtNDQwNS1iNjA0LWU3MTgxMzg5MTViZSIsIlN0ZWFtSWQiOiI5MTEwODg3NjkiLCJuYmYiOjE2Mzk5NTEyMDMsImV4cCI6MTY3MTQ4NzIwMywiaWF0IjoxNjM5OTUxMjAzLCJpc3MiOiJodHRwczovL2FwaS5zdHJhdHouY29tIn0.-ZHeanJVVGFPnR9RAkBcqPKK1CZ_c8oIYChmDwYRUog'
    
    header = {"Authorization": 'Bearer '+key1}
    url = 'https://api.stratz.com/graphql'
    
    query = """query getMatches($id: [Long]!){
            matches(ids: $id ){
                id
                rank
                sequenceNum
                lobbyType
                endDateTime
                regionId
                players{
                    steamAccountId
                    isVictory
                    hero{
                    name
                    }
                    kills
                    deaths
                    assists 
                }
            }
        }
            """
    variables= {'id': matchIds}
    r = requests.post(url,json={"query": query, 'variables': variables}, headers = header)
    print(r.status_code)
    if(r.status_code == 200):
        try:
            data = r.json()
        except Exception:
            print (Exception)
        if 'errors' in data.keys():
            print(data)
            r.status_code = 199
        
        elif data:
            if data['data']['matches']:
                newId = data['data']['matches'][0]['sequenceNum']
                if str(newId) == str(oldId):
                    newId = data['data']['matches'][(len(data['data']['matches'])-1)]['sequenceNum']
                newId = str(newId)
                try:
                    with open('dota2Private\privateApp\lastSequence.txt', "w") as myfile:
                        myfile.write(newId)
                except Exception:
                    print('File error')
                
    else:
        add_todo_to_database(matchIds)
                
    
    return r.status_code, data