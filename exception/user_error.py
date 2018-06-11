# coding:utf-8
from exception.base import TZBaseError


class UserHasExist(TZBaseError):
    code = 400
    msg = u'用户已经存在'


class TelRequire(TZBaseError):
    code = 400
    msg = u'未填写手机号'


class PasswordRequire(TZBaseError):
    code = 400
    msg = u'未填写密码'


class TelNumberError(TZBaseError):
    code = 400
    msg = u'手机号码有误'


class PasswordsDifferent(TZBaseError):
    code = 400
    msg = u'两次密码不一致'


class LoginRequire(TZBaseError):
    code = 403
    msg = u'必须登录'


class UserDoesNotExist(TZBaseError):
    code = 404
    msg = u'用户不存在'

class LoginError(TZBaseError):
    code = 404
    msg = u'手机号或密码不正确'

class UserExist(TZBaseError):
    code = 404
    msg = u'用户已存在'


class InviteUserDoesNotExist(TZBaseError):
    code = 404
    msg = u'邀请人不存在'


class AddressDoesNotExist(TZBaseError):
    code = 404
    msg = u'收货地址不存在'


class BankNameRequire(TZBaseError):
    code = 400
    msg = u'开户行不能为空'


class BankCardRequire(TZBaseError):
    code = 400
    msg = u'银行卡号不能为空'


class CardNameRequire(TZBaseError):
    code = 400
    msg = u'银行卡户名不能为空'


class ALiPayNameRequire(TZBaseError):
    code = 400
    msg = u'支付宝名称不能为空'


class ALiPayAccountRequire(TZBaseError):
    code = 400
    msg = u'支付宝账号不能为空'


class CaptchaError(TZBaseError):
    code = 400
    msg = u'验证码错误'

class CaptchaExpire(TZBaseError):
    code = 400
    msg = u'验证码过期 请重新获取'