# coding:utf-8
from exception.base import TZBaseError


class ApplyAlready(TZBaseError):
    code = 400
    msg = u'已经报过名了'


class NameRequire(TZBaseError):
    code = 401
    msg = u'未填写房间名'


class EndMustBiggerStart(TZBaseError):
    code = 401
    msg = u'结束时间必须大于开始时间'


class StartTimeRequire(TZBaseError):
    code = 401
    msg = u'未填写开始时间'


class EndTimeRequire(TZBaseError):
    code = 401
    msg = u'未填写结束时间'


class GameRequire(TZBaseError):
    code = 401
    msg = u'未选择游戏'


class GameDoesNotExist(TZBaseError):
    code = 401
    msg = u'游戏不存在'


class DescRequire(TZBaseError):
    code = 402
    msg = u'未填写描述'


class MaxCountRequire(TZBaseError):
    code = 403
    msg = u'未填写游戏人数'


class ApplyMoneyRequire(TZBaseError):
    code = 404
    msg = u'请输入报名卡数量'

class MoneyNotnough(TZBaseError):
    code = 404
    msg = u'报名卡不足请购买报名卡'