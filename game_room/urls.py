from django.conf.urls import url

from game_room.views import games, banners, room
from tz_user.views import register, phone_code, login, check_token

urlpatterns = [
    url(r'^games/$', games),
    url(r'^rooms/$', room),
    url(r'^banners/$', banners),
]
