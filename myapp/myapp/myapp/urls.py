from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('home/',include('mysite.urls')),
    path('domirecord/',include('domirecord.urls')),
    path('',RedirectView.as_view(url='home/')),

]
'''
    path('accounts/',include('accounts.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('domirecord',include('domirecord.urls')),
'''
