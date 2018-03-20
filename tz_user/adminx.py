from django.contrib import admin
from .models import TZUser, Mail
import xadmin


class TZUserAdmin(object):
    title = 'users'
    list_display = ['nickname', 'tel', 'alipay_name', 'alipay_account', 'bank_name', 'bank_account', 'bank_card_name']
    search_fields = ['nickname', 'tel', 'alipay_name']
    # list_filter = ['code', 'email', 'send_type', 'send_time']


class TZUserMailAdmin(object):
    title = 'mails'
    list_display = ['title', 'info', 'user']
    search_fields = ['title', 'user']
    # list_filter = ['code', 'email', 'send_type', 'send_time']



xadmin.site.register(TZUser, TZUserAdmin)
xadmin.site.register(Mail, TZUserMailAdmin)
