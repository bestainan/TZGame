# coding:utf-8
from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^callback/$', alipay_callback),
    # url(r'^pay/$', PayInfo.as_view(), name='alipay_pay'),
    # url(r'^refund/$', Refund.as_view(), name='alipay_refund'),
    # url(r'^query/$', Query.as_view(), name='alipay_query'),
]

