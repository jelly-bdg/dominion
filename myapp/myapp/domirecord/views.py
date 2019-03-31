from django.shortcuts import render
from django.urls import reverse_lazy,reverse
from django.views import generic
from .models import Card,Event,Player,Package,Result
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
import random
from django.utils import timezone
from .package_name_list import package_name_list_eng
from .forms import ResultForm
from django import forms
from ast import literal_eval

class IndexView(generic.TemplateView):
    template_name='domirecord/index.html'

class PlayerIndexView(generic.ListView):
    model=Player
    template_name='domirecord/player_list.html'
    def get_queryset(self):
        return Player.objects.filter(user=self.request.user)

class PlayerDetailView(generic.DetailView):
    model=Player
    template_name='domirecord/player_detail.html'

class PlayerCreateView(LoginRequiredMixin,generic.edit.CreateView):
    model=Player
    fields=['player_name','player_onoff']
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super(PlayerCreateView,self).form_valid(form)

class PlayerUpdateView(generic.edit.UpdateView):
    model=Player
    fields=['player_name','player_onoff']
    def dispatch(self,request,*args,**kwargs):
        obj=self.get_object()
        if obj.user!=self.request.user:
            raise PermissionDenied('You do not have permission to edit.')
        return super(PlayerUpdateView,self).dispatch(request,*args,**kwargs)

class PlayerDeleteView(generic.edit.DeleteView):
    model=Player
    success_url=reverse_lazy('domirecord:player_index')

class PackageDetailView(generic.DetailView):
    model=Package
    template_name='domirecord/package_detail.html'
    def get_context_data(self,**kwargs):
        package_status_dict=Package.all_package(self)
        context=super().get_context_data(**kwargs)
        context["package_status_dict"]=package_status_dict
        return context

class PackageUpdateView(generic.edit.UpdateView):
    model=Package
    fields = package_name_list_eng
    def dispatch(self,request,*args,**kwargs):
        obj=self.get_object()
        if obj.user!=self.request.user:
            raise PermissionDenied('You do not have permission to edit.')
        return super(PackageUpdateView,self).dispatch(request,*args,**kwargs)

class CardIndexView(generic.ListView):
    model=Card
    template_name='domirecord/card_list.html'

class SupplyIndexView(generic.ListView):
    model =Player
    template_name='domirecord/supply_list.html'
    def get_context_data(self,**kwargs):
        package_list=Package.select_package(self)
        context=super().get_context_data(**kwargs)
        card_list=Card.get_supply(self,package_list)
        event_list=Event.get_supply(self,package_list)
        supply={'card':card_list,'event':event_list}
        result=Result(user=self.request.user,supply=supply)
        result.save()
        context["card_list"]=card_list
        context["event_list"]=event_list
        return context

class ResultIndexView(generic.TemplateView):
    template_name='domirecord/result_list.html'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        player_list=Player.objects.filter(user=self.request.user).filter(player_onoff=True)
        result_list=Result.objects.filter(user=self.request.user).filter(finish_date__date=timezone.datetime.today()).filter(playornot=True)
        original_list=[]

        for result in result_list:
            a={}
            a['result']=literal_eval(result.player)
            a['winner']=result.winner
            original_list.append(a)

        context["player_list"]=player_list
        context["original_list"]=original_list
        return context

class ResultDetailView(generic.DetailView):
    model=Result
    template_name='domirecord/result_detail.html'
    def get_context_data(self,**kwargs):
        package_status_dict=Package.all_package(self)
        context=super().get_context_data(**kwargs)
        context["package_status_dict"]=package_status_dict
        return context


def result(request):
    r=Result.objects.filter(user=request.user).last()
    player_list=Player.objects.filter(user=request.user).filter(player_onoff=True)
    if request.method=="POST":
        player_VP={}
        for player in player_list:
            vp=request.POST.get(player.player_name)
            player_VP[player.player_name]=int(vp)
        r.player=player_VP
        r.playornot=True
        r.finish_date=timezone.datetime.now()
        r.user=request.user
        if request.POST.get('winner')!='':
            pk=int(request.POST.get('winner'))
            player=Player.objects.get(pk=pk)
            r.winner=player.player_name
        else:
            VPlow,winner=-1000,''
            for player,vp in player_VP.items():
                if VPlow<=int(vp):
                    winner=player
            r.winner=winner
        r.save()
        return HttpResponseRedirect(reverse('domirecord:index'))
    else:
        form=ResultForm()
        form.fields['winner']=forms.ModelChoiceField(required=False,label='勝利者',queryset=Player.objects.filter(user=request.user).filter(player_onoff=True),help_text='同点の場合など勝利者がいる場合入力をしてください')
        for player in player_list:
            form.fields[player.player_name]=forms.IntegerField(label=player.player_name,required=False)

        context={
            'form':form,
        }
        return render(request,'domirecord/result_form.html',context)
