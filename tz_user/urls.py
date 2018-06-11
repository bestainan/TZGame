from django.conf.urls import url
from tz_user.views import register, phone_code, login, check_token, mail, invite_user, card, forget_password, user_info

urlpatterns = [
    url(r'^register/$', register),
    url(r'^forget/password/$', forget_password),
    url(r'^login/$', login),
    url(r'^token/$', check_token),
    url(r'^info/$', user_info),
    url(r'^mail/$', mail),
    url(r'^phone/code/$', phone_code),
    url(r'^invite/$', invite_user),
    url(r'^card/$', card),
]
