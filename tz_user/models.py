# coding=utf-8
import random
import string
from .utils import *
import time

from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE, SET_NULL
from django.utils.translation import gettext_lazy as _, gettext_lazy

from TZGameServer.models import BaseTime


class TZUser(BaseTime):
    auth = models.OneToOneField(User, related_name='tz_user', on_delete=CASCADE)
    nickname = models.CharField(_('用户名'), max_length=200, null=True, blank=True)
    tel = models.CharField(_('电话号码'), max_length=20, null=True, blank=True, db_index=True)
    alipay_name = models.CharField(_('支付宝姓名'), max_length=20, null=True, blank=True)
    alipay_account = models.CharField(_('支付宝账号'), max_length=128, null=True, blank=True)
    bank_name = models.CharField(_('开户行'), max_length=128, null=True, blank=True)
    bank_account = models.CharField(_('银行卡号'), max_length=64, null=True, blank=True)
    bank_card_name = models.CharField(_('银行户名'), max_length=20, null=True, blank=True)
    money = models.IntegerField(u'余额', default=0)
    invite_user = models.ForeignKey('self', related_name='invite', null=True, blank=True, on_delete=SET_NULL)
    invite_code = models.IntegerField(default=invite_code, unique=True)
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s' % self.nickname

    def __unicode__(self):
        return '%s' % self.nickname


class Mail(BaseTime):
    title = models.CharField(_('标题'), max_length=200, null=True, blank=True)
    info = models.CharField(_('内容'), max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, related_name='mails', on_delete=CASCADE)
