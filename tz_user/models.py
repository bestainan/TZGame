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
    invite_user = models.ForeignKey('self', related_name='invite', null=True, blank=True, on_delete=CASCADE)
    invite_code = models.IntegerField('邀请码', default=invite_code, unique=True)
    card = models.IntegerField('报名卡', default=0)
    total = models.IntegerField('已赚取奖励', default=0)
    add_money = models.IntegerField('获胜者加钱', default=0)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s' % self.nickname

    def __unicode__(self):
        return '%s' % self.nickname

    def sample_data(self):
        return {
            "id": self.id,
            "tel": self.tel,
            "money": self.money,
            "nickname": self.nickname,
            "card": self.card,
            "invite_code": self.invite_code,
            "total": self.total

        }


class Mail(BaseTime):
    title = models.CharField(_('标题'), max_length=200, null=True, blank=True)
    info = models.CharField(_('内容'), max_length=200, null=True, blank=True)
    user = models.ForeignKey(TZUser, related_name='mails', on_delete=CASCADE)

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s' % self.title

    def __unicode__(self):
        return '%s' % self.title
