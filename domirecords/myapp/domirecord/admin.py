from django.contrib import admin

# Register your models here.
from .models import Player,Package,Result

admin.site.register(Player)
admin.site.register(Package)
admin.site.register(Result)
