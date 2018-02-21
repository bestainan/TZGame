# coding: utf-8

from django.db import models


BASE_STATUS_CHOICE = (
    (0, u'待审核'),
    (1, u'通过'),
    (2, u'审核拒绝'),
    (3, u'删除'),
)

YES_NO_CHOICES = (
    (0, u'NO'),
    (1, u'YES'),
)

OFFER_ORDER_GENDER = (
    (1, u'男'),
    (2, u'女'),
    (3, u'全部'),
)


class CommonManager(models.Manager):
    def get_queryset(self):
        return super(CommonManager, self).get_queryset().filter(is_delete=u'0')


class BaseTime(models.Model):
    """基本模型，带创建更新时间"""
    created = models.DateTimeField(u'创建时间', auto_now_add=True)
    updated = models.DateTimeField(u'修改时间', auto_now=True)
    is_delete = models.IntegerField(u'是否删除', choices=YES_NO_CHOICES, default=0)

    objects = CommonManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True
        ordering = ['-id', ]

    def delete(self, real_delete=False, using=None):
        if real_delete:
            super(BaseTime, self).delete(using=using)
        else:
            self.is_delete = u'1'
            self.save()

    def restore(self):
        self.is_delete = u'0'
        self.save()

