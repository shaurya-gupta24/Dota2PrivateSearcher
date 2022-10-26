from django.conf import settings
import django

from dota2Private.settings import DATABASES, INSTALLED_APPS
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
django.setup()




import time
from schedule import Scheduler
import threading
from privateApp.database_fetcher import getGamesDota2Api, getmatchesDetailsStratz
from privateApp.dabase_writer import add_to_database
from nordvpn_switcher import rotate_VPN
from django.db import connection

SECRET_KEY = 'django-insecure-uf0*ru4@iah!v($!i-(fm$4vqjd$x=!p^qeliqm$v5%n6=j4*u'

from privateApp import fetch_and_write
from privateApp.models import *
run = 0

def fetch_and_write():
    
    global run
    
    try:
        Match.objects.all().first()
    except Exception:
        connected = False
        print("database connection failed")
        connection.close()
        cursor = connection.cursor()
    else:
        connected = True
    if not run ==429 and connected == True:
        with open(r'privateApp/lastSequence.txt') as f:
            maxid = f.readline
            maxid =maxid()
        allIds=[]
        last_seq = 0
        for i in range(0,9):
            resd2, matchIds, temp_last_seq = getGamesDota2Api(maxid)
            if resd2 ==200:
                allIds+=matchIds
                last_seq = temp_last_seq
                maxid=temp_last_seq
            elif i > 2:
                break
            else:
                time.sleep(2)
               
            
        print("Found "+str(len(allIds))+" matches")
        if not len(allIds) == 0:
            print(str(allIds[len(allIds)-1]))
            chunks = [allIds[x:x+100] for x in range(0, len(allIds), 100)]
            success=True
            for chunk in chunks:
                resstratz, data = getmatchesDetailsStratz(chunk,maxid)
                run = resstratz
                if resstratz==200:
                    add_to_database(data)
                    
                    
                else: 
                    success=False
                    break
                    
            if success and last_seq!=0:
                try:
                    with open('privateApp/lastSequence.txt', "w") as myfile:
                        myfile.write(last_seq)
                except Exception as e:
                    print('File error main loop '+ str(e))
                    try:
                        with open('privateApp/lastSequence.txt', "w") as myfile:
                            myfile.write(last_seq)
                    except Exception as e:
                        print('File error main loop '+ str(e))
        elif resd2 != 200:
            time.sleep(5)
        
    else:
        if(run==429):
            rotate_VPN()
        time.sleep(30)
        run = 200
        


while True:
    fetch_and_write()
    time.sleep(1)