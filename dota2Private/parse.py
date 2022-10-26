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




while True:
    fetch_and_write.fetch_and_write()
    time.sleep(1)