from django.contrib import admin

from .models import Room, Banner, Game, Rank
import xadmin

class GamesAdmin(object):
    list_display = ['name', 'des', 'pic', 'is_hot' ]
    search_fields = ['name','is_hot']

class RoomAdmin(object):
    list_display = ['name', 'apply_money', 'max_count', 'apply']
    search_fields = ['name']

class RankAdmin(object):
    list_display = ['room', 'user', 'index']
    search_fields = ['room']

class BannerAdmin(object):
    list_display = ['link', 'des', 'pic']




xadmin.site.register(Rank, RankAdmin)
xadmin.site.register(Game, GamesAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(Room, RoomAdmin)
