from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from random import randint,sample


class Player(models.Model):
    player_name=models.CharField(max_length=100)
    player_onoff=models.BooleanField(default=True)
    user=models.ForeignKey(
    get_user_model(),
    on_delete=models.CASCADE
    )
    def __str__(self):
        return self.player_name

    def get_absolute_url(self):
        return reverse('domirecord:player_index')

class Card(models.Model):
    card_name=models.CharField(max_length=100)
    cost=models.CharField(max_length=100)
    genre=models.CharField(max_length=100)
    package=models.CharField(max_length=100)
    image=models.CharField(max_length=200)
    card_onoff=models.BooleanField(default=True)
    wikilink=models.CharField(max_length=200)
    def __str__(self):
        return self.card_name

    def get_supply(self,package_list):
        card_list=[card for card in Card.objects.filter(package__in=package_list)]
        card_number=[i for i in range(len(card_list))]
        card_index=sample(card_number,10)
        card_index.sort()
        a=[]
        for number in card_index:
            a.append(card_list[number])
        return a

class Event(models.Model):
    event_name=models.CharField(max_length=100)
    cost=models.CharField(max_length=100)
    genre=models.CharField(max_length=100)
    package=models.CharField(max_length=100)
    image=models.CharField(max_length=200)
    event_onoff=models.BooleanField(default=True)
    wikilink=models.CharField(max_length=200)
    def __str__(self):
        return self.event_name
    def get_supply(self,package_list):
        event_list=[event for event in Event.objects.filter(package__in=package_list)]
        event_number=[i for i in range(len(event_list))]
        number=randint(0,2)
        event_index=sample(event_number,number)
        event_index.sort()
        a=[]
        for number in event_index:
            a.append(event_list[number])
        return a

class Package(models.Model):
    user=models.OneToOneField(
    get_user_model(),
    on_delete=models.CASCADE
    )
    basic=models.BooleanField(default=True)
    intrigue=models.BooleanField(default=True)
    seaside=models.BooleanField(default=True)
    alchemy=models.BooleanField(default=True)
    prosperity=models.BooleanField(default=True)
    cornucopia=models.BooleanField(default=True)
    hinterlands=models.BooleanField(default=True)
    darkage=models.BooleanField(default=True)
    guild=models.BooleanField(default=True)
    adventures=models.BooleanField(default=True)
    empires=models.BooleanField(default=True)
    nocturne=models.BooleanField(default=True)
    def __str__(self):
        return self.user.username+' package'

    def get_absolute_url(self):
        return reverse('domirecord:index')

    def select_package(self):
        package=Package.objects.values("basic","intrigue","seaside","alchemy","prosperity","cornucopia","hinterlands","darkage","guild","adventures","empires","nocturne").get(user=self.request.user)
        package_list=[]
        package_name_list_eng=["basic","intrigue","seaside","alchemy","prosperity","cornucopia","hinterlands","darkage","guild","adventures","empires","nocturne"]
        package_dict_engja={'basic': '基本',
         'intrigue': '陰謀',
         'seaside': '海辺',
         'alchemy': '錬金術',
         'prosperity': '繁栄',
         'cornucopia': '収穫祭',
         'hinterlands': '異郷',
         'darkage': '暗黒時代',
         'guild': 'ギルト',
         'adventures': '冒険',
         'empires': '帝国',
         'nocturne': '夜想曲'}
        for name in package_name_list_eng:
            if package.get(name):
                package_list.append(package_dict_engja[name])
        return package_list

@receiver(post_save, sender=get_user_model())
def create_user_package(sender, instance, created, **kwargs):
    if created:
        Package.objects.create(user=instance)

@receiver(post_save, sender=get_user_model())
def save_user_package(sender, instance, **kwargs):
    instance.package.save()

'''

class Result(models.Model):
    supply=models.CharField(max_length=200)
    player=models.CharField(max_length=200)
    winner=models.CharField(max_length=100)
    playornot=models.BooleanField(default=False)
    finish_date=models.DateTimeField(default=timezone.now)
    user=models.ForeignKey(
    get_user_model(),
    models.PROTECT
    )


'''
