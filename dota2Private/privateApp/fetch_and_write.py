from .database_fetcher import getGamesDota2Api, getmatchesDetailsStratz
from .dabase_writer import add_to_database
from nordvpn_switcher import rotate_VPN

import time
from schedule import Scheduler
import threading
from .models import todo, Match
from django.db import connections
from django.db.utils import OperationalError
from django.db import connection
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
        with open(r'privateApp\lastSequence.txt') as f:
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
                    with open('privateApp\lastSequence.txt', "w") as myfile:
                        myfile.write(last_seq)
                except Exception as e:
                    print('File error main loop '+ str(e))
                    try:
                        with open('privateApp\lastSequence.txt', "w") as myfile:
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
        
def clean_todo():
    for e in todo.objects.values_list('match_id', flat=True).distinct():
        todo.objects.filter(pk__in=todo.objects.filter(match_id=e).values_list('match_id', flat=True)[1:]).delete()
        print(e)        


    

def run_continuously(self, interval=1):
        """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """

        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):

            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    self.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.setDaemon(True)
        continuous_thread.start()
        return cease_continuous_run

Scheduler.run_continuously = run_continuously

def start_scheduler():
    scheduler = Scheduler()
    scheduler.every().second.do(fetch_and_write)
    scheduler.run_continuously()