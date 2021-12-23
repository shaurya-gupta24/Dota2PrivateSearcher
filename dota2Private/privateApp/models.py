from django.db import models
from django.db.models.deletion import CASCADE

from dota2Private.settings import DEFAULT_AUTO_FIELD

# Create your models here.
class Match(models.Model):
    matchId = models.BigIntegerField(unique=True, primary_key=True)
    rank = models.BigIntegerField()
    sequenceNum=models.BigIntegerField()
    end_time = models.BigIntegerField()
    lobby_type=models.IntegerField()
    
class Player(models.Model):
    player_id = models.BigIntegerField()
    match_id = models.ForeignKey(Match, on_delete=CASCADE)
    victory = models.CharField(max_length=5)
    hero = models.CharField(max_length=30)
    kills= models.BigIntegerField()
    deaths = models.BigIntegerField()
    assists = models.BigIntegerField()
    
class todo(models.Model):
    match_id = models.BigIntegerField()
    