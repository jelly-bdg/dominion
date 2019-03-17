from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
# Create your models here.
class Player(models.Model):
    player_name=models.CharField(max_length=100)
    player_onoff=models.BooleanField()
    user=models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.player_name

'''
class Card(models.Model):

    card_name=models.CharField(max_length=100)
    cost=models.CharField(max_length=100)
    genre=models.CharField(max_length=100)
    package=models.CharField(max_length=100)
    image=models.CharField(max_length=200)
    card_onoff=models.BooleanField(default=True)
    wikilink=models.CharField(max_length=200)

class Event(models.Model):

    event_name=models.CharField(max_length=100)
    cost=models.CharField(max_length=100)
    genre=models.CharField(max_length=100)
    package=models.CharField(max_length=100)
    image=models.CharField(max_length=200)
    event_onoff=models.BooleanField(default=True)
    wikilink=models.CharField(max_length=200)
'''

class Result(models.Model):
    supply=models.CharField(max_length=200)
    player=models.CharField(max_length=200)
    winner=models.CharField(max_length=100)
    playornot=models.BooleanField(default=False)
    finish_date=models.DateTimeField(default=timezone.now)
    user=models.CharField(max_length=200,default='kamenbutokai')
class Package(models.Model):
    package_name=models.CharField(max_length=20)
    package_onoff=models.BooleanField()
    user=models.CharField(max_length=200,default='kamenbutokai')
    def __str__(self):
        return self.package_name
