from django.conf.urls import url

from game_room.views import rooms, banners
from tz_user.views import register, phone_code, login, check_token

urlpatterns = [
    url(r'^rooms/$', rooms),
    url(r'^banners/$', banners),
]
