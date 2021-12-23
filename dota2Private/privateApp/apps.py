from django.apps import AppConfig
import os

class PrivateappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'privateApp'

    def ready(self):
        from . import fetch_and_write
        if os.environ.get('RUN_MAIN', None) != 'true':
            fetch_and_write.start_scheduler()