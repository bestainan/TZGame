# coding=utf-8
import random
import string

import time

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _, gettext_lazy

from TZGameServer.models import BaseTime
from tz_user.models import TZUser


class Room(BaseTime):
    name = models.CharField(_('房间名称'), max_length=200, null=True, blank=True)
    apply_money = models.IntegerField(_('报名费'))
    pic = models.CharField(_('图片地址'), max_length=200, null=True, blank=True)
    max_count = models.CharField(_('最大人数'), max_length=20, null=True, blank=True)
    current_count = models.CharField(_('当前人数'), max_length=128, null=True, blank=True)
    apply = models.ManyToManyField(TZUser, related_name='room', verbose_name='报名信息', null=True, blank=True)

    class Meta:
        verbose_name = '房间信息'
        verbose_name_plural = verbose_name

class Banner(BaseTime):
    link = models.CharField('跳转链接', max_length=256, null=True, blank=True)
    pic = models.CharField('图片地址', max_length=256, null=True, blank=True)
    des = models.CharField('描述', max_length=64, null=True, blank=True)

    class Meta:
        verbose_name = '导航广告'
        verbose_name_plural = verbose_name
    def __str__(self):
        return '%s' % self.des

    def __unicode__(self):
        return '%s' % self.des