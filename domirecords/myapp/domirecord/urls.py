from django.urls import path
from . import views
app_name='domirecord'

urlpatterns=[
    path('',views.Index.as_view(),name='index'),
    path('player/',views.player,name='player'),
    path('addplayer',views.addplayer,name='addplayer'),
    path('select',views.select,name='select'),
    path('gamestart',views.gamestart,name='gamestart'),
    path('result',views.result,name='result'),
    path('record',views.RecordList.as_view(),name='record')
]
