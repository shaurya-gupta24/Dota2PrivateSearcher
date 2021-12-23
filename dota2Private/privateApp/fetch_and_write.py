from .database_fetcher import getGamesDota2Api, getmatchesDetailsStratz
from .dabase_writer import add_to_database

import time
from schedule import Scheduler
import threading
run = 200

def fetch_and_write():
    global run
    if not run ==429:
        with open(r'dota2Private\privateApp\lastSequence.txt') as f:
            maxid = f.readline
            maxid =maxid()
        matchIds = []
        resd2, matchIds = getGamesDota2Api(maxid,matchIds)
        if resd2 == 200:
            chunks = [matchIds[x:x+10] for x in range(0, len(matchIds), 10)]
            for chunk in chunks:
                resstratz, data = getmatchesDetailsStratz(chunk,maxid)
                run = resstratz
            
                if resstratz==200:
                    add_to_database(data)
                else: break
        
        elif resd2 != 200:
            time.sleep(5)
        
    else:
        time.sleep(900)
        run = 200
        
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