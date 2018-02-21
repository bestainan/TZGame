from django.conf.urls import url
from tz_user.views import register, phone_code, login, check_token

urlpatterns = [
    url(r'^register/$', register),
    url(r'^login/$', login),
    url(r'^token/$', check_token),

    url(r'^phone/code/$', phone_code),

]
