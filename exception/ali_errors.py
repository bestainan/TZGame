#coding:utf-8
from exception.base import TZBaseError

class OrderIdCanNotBeNull(TZBaseError):
    code = 403
    msg = u'订单号不能为空'

class OrderIdDoesNotExist(TZBaseError):
    code = 404
    msg = u'订单不存在'