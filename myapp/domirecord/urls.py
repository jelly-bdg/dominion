from django.urls import path
from . import views
app_name='domirecord'


urlpatterns=[
    path('',views.IndexView.as_view(),name='index'),
    path('package/<int:pk>',views.PackageDetailView.as_view(),name='package_detail'),
    path('package/<int:pk>/update/',views.PackageUpdateView.as_view(),name='package_update'),
    path('player/',views.PlayerIndexView.as_view(),name='player_index'),
    path('player/<int:pk>',views.PlayerDetailView.as_view(),name='player_detail'),
    path('player/create',views.PlayerCreateView.as_view(),name='player_create'),
    path('player/<int:pk>/update/',views.PlayerUpdateView.as_view(),name='player_update'),
    path('player/<int:pk>/delete/',views.PlayerDeleteView.as_view(),name='player_delete'),
    path('card/',views.CardIndexView.as_view(),name='card_list'),
    path('supply/',views.SupplyIndexView.as_view(),name='supply_index'),
]
