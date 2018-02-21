# coding: utf-8
import re

def check_phone(phone):
    """检查手机号号码"""
    if phone and isinstance(phone, str) and phone.isdigit():
        p = re.compile(r'1(3|4|5|6|7|8)\d{9}$')
        if p.match(phone):
            return True
    return False