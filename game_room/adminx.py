from django.contrib import admin
from .models import Room, Banner
import xadmin


class RoomAdmin(object):
    list_display = ['name', 'apply_money', 'max_count', 'current_count', 'apply', ]
    search_fields = ['name']


class BannerAdmin(object):
    list_display = ['link', 'des', 'pic']


xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(Room, RoomAdmin)
