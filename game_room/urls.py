from django.conf.urls import url

from game_room.views import games, banners, room, room_info, apply_history, room_apply, room_apply_balance, upload_img
from tz_user.views import register, phone_code, login, check_token

urlpatterns = [
    url(r'^games/$', games),
    url(r'^rooms/$', room),
    url(r'^room/$', room_info),
    url(r'^banners/$', banners),
    url(r'^apply/history/$', apply_history),
    url(r'^room_apply/alipay/$', room_apply),
    url(r'^room_apply/balance/$', room_apply_balance),
    url(r'^upload_img/$', upload_img),


]
