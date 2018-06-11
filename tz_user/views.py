# # coding:utf-8
import random

import time
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import IntegrityError
from django.db.models import Sum
from django.http import JsonResponse
from django.utils import timezone
import base64
from django.contrib.auth import login  as auth_login
from django.utils.six import b
from django.views.decorators.http import require_POST, require_GET

from TZGameServer.middlewares import auth_required
from TZGameServer.utils import AliyunSMS
from exception.base import TZBaseError
from exception.user_error import UserExist, UserDoesNotExist, LoginError
from game_room.models import ApplyDetail
from tz_user.forms import SignUpForm, ForgetPasswordForm
import hashlib
from tz_user.models import TZUser, Mail


@require_POST
def login(request):
    data = {'code': 1, 'error': '', 'data': {}}
    tel = request.POST.get('tel')
    password = request.POST.get('password')
    try:
        user = authenticate(username=tel, password=password)
        if not user:
            raise LoginError()
        auth_login(request, user)
        data['data'] = user.tz_user.sample_data()

    except TZBaseError as e:
        data['code'] = e.code
        data['msg'] = e.msg
    return JsonResponse(data=data)


import psycopg2


@require_GET
def check_token(request):
    data = {}
    token = request.GET.get('tztoken')
    session = Session.objects.filter(session_key=token).first()
    if not session:
        data['code'] = 404
    else:
        user_id = session.session_data
        user = TZUser.objects.filter(pk=user_id).first()
        if user:
            data['code'] = 1
            data['data'] = {
                'id': user.id,
                'invite_code': user.invite_code,
                'nickname': user.nickname,
                'tel': user.tel,
                'card': user.card,
            }
        else:
            data['code'] = 404
    return JsonResponse(data=data)


@require_POST
def phone_code(request):
    data = {}
    tel = request.POST.get('tel', '')
    try:
        if request.method == 'POST':
            if not tel:
                data['code'] = 400
                data['msg'] = '请填写手机号'
            else:
                v_code = random.randint(1000, 9999)
                print(v_code)
                cli = AliyunSMS(access_key_id='LTAIumaptAEoL3Xr', access_secret='xgQgKuSZ8RvOIMxrk8e7eqSHejqtza')
                cli.request(phone_numbers=tel,
                            sign='王者挑战赛',
                            template_code='SMS_126260131',
                            template_param={'code': str(v_code)})
                request.session['v_code_expire_time'] = timezone.now() + timezone.timedelta(seconds=60)
                request.session['v_code'] = v_code
                data['code'] = 1
    except TZBaseError as e:
        data['code'] = e.code
        data['msg'] = e.msg
    return JsonResponse(data=data)


@require_POST
def register(request):
    signup_form = SignUpForm(request.POST, request=request)
    data = {}
    try:
        if signup_form.is_valid():
            user = signup_form.save()
            data['data'] = user.sample_data()
            data['code'] = 1

        else:
            print(signup_form.errors)
    except TZBaseError as e:
        data['msg'] = e.msg
        data['code'] = e.code
    return JsonResponse(data=data)


@auth_required
def user_info(request):
    data = {'code': 1}
    data['data'] = request.user.tz_user.sample_data()
    return JsonResponse(data=data)


@require_POST
def forget_password(request):
    form = ForgetPasswordForm(request.POST, request=request)
    data = {}
    try:
        if form.is_valid():
            user = form.save()
            data['data'] = user.sample_data()
            data['code'] = 1
            auth_login(request, user.auth)
        else:
            print(form.errors)
    except TZBaseError as e:
        data['msg'] = e.msg
        data['code'] = e.code
    return JsonResponse(data=data)


@require_GET
@auth_required
def mail(request):
    data = []
    user = request.user
    mails = Mail.objects.filter(user=user.tz_user).order_by('-id')
    for _mail in mails:
        data.append({
            'id': _mail.id,
            'date': _mail.created.strftime("%Y-%m-%d %H:%M:%S"),
            'title': _mail.title,
            'desc': _mail.info,
            'user': _mail.user.nickname,
        })
    return JsonResponse(data={'data': data})


@require_GET
@auth_required
def invite_user(request):
    data = []
    user_id = request.GET.get('user_id')
    invite_users = TZUser.objects.filter(invite_user=user_id)
    for _u in invite_users:
        data.append(
            {
                'name': _u.nickname,
                'count': TZUser.objects.filter(invite_user=_u.id).count(),
                'apply_money': ApplyDetail.objects.filter(user=_u).aggregate(Sum('money'))['money__sum'] or 0
            }
        )
    return JsonResponse(data={'data': data})


@require_POST
@auth_required
def card(request):
    data = {"code": 1, "data": {}}
    card_type = int(request.POST.get('card_type'))
    user = request.user.tz_user
    data['code'] = 1

    if user.card >= 5:
        data['code'] = 101
        data['msg'] = f'您还有{user.card}张未使用，暂时不能领取'
    else:
        if card_type == 5:
            user.card += 5
            data['data']['count'] = 5
        elif card_type == 2:
            user.card += 2
            data['data']['count'] = 2
        else:
            user.card += 1
            data['data']['count'] = 1
        user.save()
    return JsonResponse(data)
