# coding:utf-8
import traceback

import datetime


class TZBaseError(Exception):
    code = -1
    msg = u'系统错误'

    def __init__(self, *args, **kwargs):
        self.code = self.code
        self.msg = self.msg

    def __str__(self):
        return self.msg
