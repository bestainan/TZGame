# coding=utf-8
import random
import string

import time

from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _, gettext_lazy

from TZGameServer.models import BaseTime
from tz_user.models import TZUser


class Game(BaseTime):
    name = models.CharField(_('游戏名称'), max_length=200, null=True, blank=True)
    des = models.CharField(_('描述'), max_length=200, null=True, blank=True)
    pic = models.CharField(_('图片地址'), max_length=200, null=True, blank=True)
    is_hot = models.IntegerField(_('热门'), default=0)

    class Meta:
        verbose_name = '游戏列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s' % self.name

    def __unicode__(self):
        return '%s' % self.name


ROOM_STATUS = (
    (1, u'未开始'),
    (2, u'进行中'),
    (2, u'已结束'),
)


class Room(BaseTime):
    name = models.CharField(_('房间名称'), max_length=200, null=True, blank=True)
    apply_money = models.IntegerField(_('报名费'))
    hot = models.BooleanField(default=False)
    status = models.IntegerField(u'状态', choices=ROOM_STATUS, default=1)
    pic = models.CharField(_('图片地址'), max_length=200, null=True, blank=True)
    des = models.TextField(_('描述'), max_length=200, null=True, blank=True)
    max_count = models.IntegerField(_('最大人数'))
    current_count = models.IntegerField(_('当前人数'), default=0, null=True, blank=True)
    apply = models.ManyToManyField(TZUser, related_name='room', verbose_name='报名信息', null=True, blank=True)
    game = models.ForeignKey(Game, related_name='rooms', null=True, blank=True, on_delete=CASCADE)

    class Meta:
        verbose_name = '房间信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s' % self.name

    def __unicode__(self):
        return '%s' % self.name


class Rank(BaseTime):
    room = models.ForeignKey(Room, related_name='rank', null=True, blank=True, on_delete=CASCADE)
    user = models.ForeignKey(TZUser, null=True, blank=True, on_delete=CASCADE)
    index = models.IntegerField(_('排名'))

    class Meta:
        verbose_name = '房间排行'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s' % self.room.name

    def __unicode__(self):
        return '%s' % self.room.name


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


APPLY_STATUS = (
    (0, u'已完成'),
    (1, u'待支付'),
    (2, u'支付中'),
    (3, u'支付失败'),
)
def order_oid():
    return str(int(time.time() * 1000)) + str(int(random.random() * 1000000))


class ApplyDetail(BaseTime):
    id = models.CharField('订单id',max_length=256, default=order_oid, primary_key=True)
    money = models.IntegerField(_('报名金额'))
    user = models.ForeignKey(TZUser, null=True, blank=True, on_delete=CASCADE)
    room = models.ForeignKey(Room, related_name='apply_detail', null=True, blank=True, on_delete=CASCADE)
    status = models.IntegerField(u'状态', choices=APPLY_STATUS, default=1)

    class Meta:
        verbose_name = '报名明细'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s' % self.user.nickname

    def __unicode__(self):
        return '%s' % self.user.nickname




ORDER_TYPE = (
    (1, u'游戏房间报名'),
    (2, u'充值'),

)


# class Order(BaseTime):
#     money = models.IntegerField(_('金额'))
#     type = models.IntegerField(u'类型', choices=ROOM_STATUS, default=1)
#     status = models.IntegerField(u'状态', choices=ORDER_STATUS, default=1)
#
