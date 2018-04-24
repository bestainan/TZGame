# # coding:utf-8
import random

import time

from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session
from django.db import IntegrityError
from django.db.models import Sum
from django.http import JsonResponse
from django.utils import timezone
import base64

from django.utils.six import b
from django.views.decorators.http import require_POST, require_GET

from TZGameServer.middlewares import auth_required
from TZGameServer.utils import AliyunSMS
from exception.base import TZBaseError
from exception.user_error import UserExist
from game_room.models import ApplyDetail
from tz_user.forms import SignUpForm
import hashlib
from tz_user.models import TZUser, Mail


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
        Session.objects.update_or_create(session_key=base64_code, defaults={'session_data': user.tz_user.id, 'expire_date': expire_time})
        data['data'] = {
            'id': user.tz_user.id,
            'invite_code': user.tz_user.invite_code,
            'nickname': user.tz_user.nickname,
            'tel': user.tz_user.tel,
            'tztoken': base64_code,
            'card': user.tz_user.card,
        }
    else:
        data['code'] = 404
        data['msg'] = '用户不存在'
    return JsonResponse(data=data)


@require_GET
def check_token(request):
    data = {}
    print(request.COOKIES)
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


# @require_POST
def phone_code(request):
    data = {}
    tel = request.GET.get('tel', '') or request.POST.get('tel', '')
    user = TZUser.objects.filter(tel=tel)
    try:
        if user:
            raise UserExist()
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
                import logging
                logger = logging.getLogger("django")  # 为loggers中定义的名称
                logger.info(v_code)
                cli = AliyunSMS(access_key_id='LTAIumaptAEoL3Xr', access_secret='xgQgKuSZ8RvOIMxrk8e7eqSHejqtza')
                cli.request(phone_numbers=tel,
                            sign='王者挑战赛',
                            template_code='SMS_126260131',
                            template_param={'code': str(v_code)})
                # 存session
                expire_time = timezone.now() + timezone.timedelta(seconds=60)
                Session.objects.create(session_key=tel, session_data=v_code, expire_date=expire_time)
                data['code'] = 1
    except TZBaseError as e:
        data['code'] = e.code
        data['msg'] = e.msg
    return JsonResponse(data=data)


@require_POST
def register(request):
    signup_form = SignUpForm(request.POST)
    data = {}
    try:
        if signup_form.is_valid():
            user = signup_form.save(commit=True)
            data['code'] = 1
            expire_time = timezone.now() + timezone.timedelta(days=3)
            md5 = hashlib.md5()
            md5.update(user.tel.encode("utf8"))
            base64_code = md5.hexdigest()
            Session.objects.create(session_key=base64_code, session_data=user.id, expire_date=expire_time)

            data['data'] = {
                'id': user.id,
                'token': base64_code,
                'tel': user.tel,
                'nickname': user.nickname,
                'invite_code': user.invite_code,
                'card': user.card,
            }
        else:
            print(signup_form.errors)
    except TZBaseError as e:
        data['msg'] = e.msg
        data['code'] = e.code
    return JsonResponse(data=data)


@require_GET
@auth_required
def mail(request):
    data = []
    user = request.user
    print(user)
    mails = Mail.objects.filter(user=user)
    for _mail in mails:
        data.append({
            'id': _mail.id,
            'meta': {
                'date': _mail.created.strftime("%Y-%m-%d %H:%M:%S"),
            },
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
    data = {}
    card_type = request.POST.get('card_type')
    user = request.user
    print(card_type)
    if card_type == 5:
        user.card += 5
    elif card_type == 2:
        user.card += 2
    else:
        user.card += 1
    user.save()
    data['code'] = 1
    return JsonResponse(data={'data': data})
