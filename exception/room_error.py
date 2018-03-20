# coding:utf-8
from exception.base import TZBaseError


class ApplyAlready(TZBaseError):
    code = 400
    msg = u'已经报过名了'

