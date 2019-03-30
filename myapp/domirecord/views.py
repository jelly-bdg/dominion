from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import Card,Event,Player,Package,Result
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
import random
from .package_name_list import package_name_list_eng

class IndexView(generic.TemplateView):
    template_name='domirecord/index.html'

class PlayerIndexView(generic.ListView):
    model=Player
    template_name='domirecord/player_list.html'

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
