from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from .models import Player,Package,Result
from django.views.generic import TemplateView,ListView,CreateView
from accounts.models import CustomUser
from django.utils.functional import cached_property
from .CardNameDict import cardnamedict,eventnamedict
import random
import ast#文字列から辞書
from collections import defaultdict
# Create your views here.

class Index(TemplateView):
    template_name="domirecord/index.html"
    @cached_property
    def player(self):
        return Player.objects.filter(user=self.request.user).filter(player_onoff=True)
    def package(self):
        return Package.objects.filter(user=self.request.user).filter(package_onoff=True)

class RecordList(ListView):
    template_name='domirecord/record.html'
    @cached_property
    def record(self):
        result=Result.objects.filter(user=self.request.user).filter(playornot=True)[:5]
        output=[]
        for r in result:
            recorddict={}
            supply=ast.literal_eval(r.supply)
            recorddict['used_card_list']=supply['card']
            recorddict['used_event_list']=supply['event']
            output.append(recorddict)
        context={
            'output':output,
        }

        return render(self.request,'domirecord.html',context)

def player(request):
    if request.method=='POST':
        select_player=request.POST.getlist('select')
        for player in select_player:
            change_player=Player.objects.get(player_name=player)
            if change_player.player_onoff:
                change_player.player_onoff=False
            else:
                change_player.player_onoff=True
            change_player.save()
        return HttpResponseRedirect(reverse('domirecord:index'))
    else:
        User=request.user.id
        player=Player.objects.filter(user_id=User)
        context={
            'player':player,
        }
        return render(request,'domirecord/player.html',context)

def addplayer(request):
    if request.method=='POST':
        add_player=request.POST.get('addplayer')
        User=request.user
        player=Player(player_name=add_player,player_onoff=True,user=User)
        player.save()
        return HttpResponseRedirect(reverse('domirecord:index'))
    else:
        return render(request,'domirecord/addplayer.html')

def select(request):
    User=request.user
    if request.method=="POST":
        select_package=request.POST.getlist('select')

        for package in select_package:
            change_package=Package.objects.filter(user=User).get(package_name=package)
            if change_package.package_onoff:
                change_package.package_onoff=False
            else:
                change_package.package_onoff=True
            change_package.save()
        return HttpResponseRedirect(reverse('domirecord:index'))
    else:
        package_list=Package.objects.filter(user=request.user)
        context={
        'package_list':package_list,
        }
        return render(request,'domirecord/select.html',context)

def gamestart(request):
    User=request.user
    package_list=Package.objects.filter(user=User)
    player=Player.objects.filter(user=User).filter(player_onoff=True)
    recent_record=Result.objects.filter(user=User).filter(finish_date__date=timezone.datetime.today()).filter(playornot=True)
    gamecount=1
    winner=defaultdict()
    for record in recent_record:
        gamecount+=1
        try:
            winner[record.winner]
        except:
            winner[record.winner]=1
        else:
            winner[record.winner]+=1


    use_package_list=Package.objects.filter(user=User).filter(package_onoff=True)
    usecards=[]
    useevents=[]
#使う王国カード
    for package in use_package_list:
        for card in cardnamedict[str(package)]:
            usecards.append(card)
            #使うイベントカード
    for package in use_package_list:
        for event in eventnamedict[str(package)]:
            useevents.append(event)
#使うカード群から王国カード,イベントカードを選択
    selectcards=random.sample(usecards,10)
    eventnumber=random.randint(0,2)
    try:
        random.sample(useevents,eventnumber)
    except:
        selectevents=[]
    else:
        selectevents=random.sample(useevents,eventnumber)
#id順に並び替え
    sortid=lambda val:int(val[0])
    selectcards.sort(key=sortid)
    selectevents.sort(key=sortid)
    supply={}
    supply['card']=selectcards
    supply['event']=selectevents
    players=Player.objects.filter(user=User).filter(player_onoff=True)
    player=[]
    for p in players:
        player.append(p.player_name)
    r=Result(supply=supply,player=player,user=request.user)
    r.save()

    context={
        'selectcards':selectcards,
        'selectevents':selectevents,
        'player':player,
        'gamecount':gamecount,
        'winner':winner,
    }
    return render(request,'domirecord/gamestart.html',context)

def result(request):
    r=Result.objects.filter(user=request.user).last()
    supply=ast.literal_eval(r.supply)
    used_card_list=supply['card']
    used_event_list=supply['event']
    player=ast.literal_eval(r.player)
    if request.method=="POST":
        VP=request.POST.getlist('VP')
        player_VP=dict(zip(player,VP))
        r.player=player_VP
        max=-1000
        winner=''
        for p in player:
            if int(player_VP[p])>=max:
                max=int(player_VP[p])
                winner=p
        r.winner=winner
        r.playornot=True
        r.finish_date=timezone.datetime.now()
        r.save()
        return HttpResponseRedirect(reverse('domirecord:gamestart'))
    else:
        User=request.user
        recent_record=Result.objects.filter(user=User).filter(finish_date__date=timezone.datetime.today()).filter(playornot=True)
        gamecount=1
        for record in recent_record:
            gamecount+=1

        context={
            'used_card_list':used_card_list,
            'used_event_list':used_event_list,
            'player':player,
            'gamecount':gamecount,
        }
        return render(request,'domirecord/result.html',context)
