from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import Card,Event,Player,Package
import random

class IndexView(generic.TemplateView):
    template_name='domirecord/index.html'

class PlayerIndexView(generic.ListView):
    model=Player
    template_name='domirecord/player_list.html'

class PlayerDetailView(generic.DetailView):
    model=Player
    template_name='domirecord/player_detail.html'

class PlayerCreateView(generic.edit.CreateView):
    model=Player
    fields='__all__'

class PlayerUpdateView(generic.edit.UpdateView):
    model=Player
    fields='__all__'

class PlayerDeleteView(generic.edit.DeleteView):
    model=Player
    success_url=reverse_lazy('domirecord:player_index')

class PackageDetailView(generic.DetailView):
    model=Package
    template_name='domirecord/package_detail.html'

class PackageUpdateView(generic.edit.UpdateView):
    model=Package
    fields = '__all__'

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
        context["card_list"]=card_list
        context["event_list"]=event_list
        return context
