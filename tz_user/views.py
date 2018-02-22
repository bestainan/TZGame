# # coding:utf-8
import random

import time

from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils import timezone
import base64

from django.utils.six import b
from django.views.decorators.http import require_POST, require_GET

from TZGameServer.utils import AliyunSMS
from exception.base import TZBaseError
from tz_user.forms import SignUpForm
import hashlib
from tz_user.models import TZUser


@require_POST
def login(request):
    data = {}
    tel = request.POST.get('tel')
    password = request.POST.get('password')
    user = authenticate(username=tel, password=password)
    if user:
        md5 = hashlib.md5()
        md5.update(user.username.encode("utf8"))
        base64_code = md5.hexdigest()
        expire_time = timezone.now() + timezone.timedelta(days=7)
        Session.objects.create(session_key=base64_code, session_data=user.tz_user.id, expire_date=expire_time)
        data['data'] = {
            'nickname': user.tz_user.nickname,
            'tel': user.tz_user.tel,
            'token': base64_code,
        }
    else:
        data['code'] = 404
        data['msg'] = '用户不存在'
    return JsonResponse(data=data)


@require_GET
def check_token(request):
    data = {}
    token = request.GET.get('token')
    session = Session.objects.filter(session_key=token).first()
    if not session:
        data['code'] = 404
    else:
        user_id = session.session_data
        user = TZUser.objects.filter(pk=user_id).first()
        if user:
            data['code'] = 1
            data['data'] = {
                'nickname': user.nickname,
                'tel': user.tel
            }
        else:
            data['code'] = 404
    return JsonResponse(data=data)


# @require_POST
def phone_code(request):
    data = {}
    tel = request.GET.get('tel', '') or request.POST.get('tel', '')

    if request.method == 'GET':
        v_code = request.GET.get('code', '')
        # 取session

        session_key = Session.objects.filter(session_key=tel).first()
        if not session_key:
            data['code'] = 400
            data['msg'] = '验证码过期'
        elif not tel:
            data['code'] = 400
            data['msg'] = '请填写手机号'
        elif session_key.session_data == v_code:
            # 验证成功
            data['code'] = 1
        else:
            data['code'] = 400
            data['msg'] = '验证码错误'

    if request.method == 'POST':
        sission_time = Session.objects.filter(session_key=tel).first()
        if sission_time:
            ex_time = int(time.mktime(sission_time.expire_date.timetuple()))
            if (time.time() - ex_time) > 60:
                sission_time.delete()
            else:
                data['code'] = 400
                data['msg'] = '操作太频繁'
                return JsonResponse(data=data)
        if not tel:
            data['code'] = 400
            data['msg'] = '请填写手机号'
        else:
            v_code = random.randint(1000, 9999)
            # todo:阿里云发送验证码逻辑
            print(v_code)
            cli = AliyunSMS(access_key_id='LTAIumaptAEoL3Xr', access_secret='xgQgKuSZ8RvOIMxrk8e7eqSHejqtza')
            cli.request(phone_numbers='18777777105',
                               sign='王者挑战赛',
                               template_code='SMS_126260131',
                               template_param={'code': str(v_code)})
            # 存session
            expire_time = timezone.now() + timezone.timedelta(seconds=60)
            Session.objects.create(session_key=tel, session_data=v_code, expire_date=expire_time)
            data['code'] = 1
    return JsonResponse(data=data)


@require_POST
def register(request):
    """达人微信快捷注册"""
    signup_form = SignUpForm(request.POST)
    data = {}
    try:
        if signup_form.is_valid():
            user = signup_form.save(commit=True)
            data['code'] = 1
            expire_time = timezone.now() + timezone.timedelta(days=7)
            md5 = hashlib.md5()
            md5.update(user.tel.encode("utf8"))
            base64_code = md5.hexdigest()
            Session.objects.create(session_key=base64_code, session_data=user.id, expire_date=expire_time)

            data['data'] = {
                'token': base64_code,
                'tel': user.tel,
                'nickname': user.nickname,
            }
        else:
            print(signup_form.errors)
    except TZBaseError as e:
        data['msg'] = e.msg
        data['code'] = e.code
    return JsonResponse(data=data)
