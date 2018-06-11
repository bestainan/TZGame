# # coding:utf-8
import hashlib
import json

import os
import random

import time

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET

from TZGameServer.middlewares import auth_required
from exception.base import TZBaseError
from exception.room_error import ApplyAlready, MoneyNotnough
from game_room.forms import CreateRoomForm
from game_room.models import Room, Banner, Game, ApplyDetail, CheckWinner
from tz_user.models import TZUser, Mail


@require_GET
@auth_required
def games(request):
    data = []
    is_hot = request.GET.get('hot')
    if is_hot:
        games = Game.objects.filter(is_hot=1)
    else:
        games = Game.objects.all()
    for _game in games:
        data.append({
            'id': _game.id,
            'name': _game.name,
            'des': _game.des,
            'pic': _game.pic,
        })
    return JsonResponse(data={'data': data})


@require_GET
@auth_required
def room(request):
    game_id = request.GET.get('game_id')
    hot = request.GET.get('hot')
    data = []
    if hot:
        rooms = Room.objects.filter(hot=True)
    else:
        rooms = Room.objects.filter(game_id=game_id)
    for room in rooms:
        data.append({
            'id': room.id,
            'name': room.name,
            'hot': room.hot,
            'apply_money': room.apply_money,
            'pic': room.pic,
            'max_count': room.max_count,
            'current_count': room.current_count,
        })
    return JsonResponse(data={'data': data})

@require_POST
@auth_required
def create_room(request):
    form = CreateRoomForm(request.POST)
    data = {"code":1,"msg":''}
    try:
        if form.is_valid():
            room = form.save()
            data['data'] = {
                'id': room.id,
            }
        else:
            print(form.errors)
    except TZBaseError as e:
        data['msg'] = e.msg
        data['code'] = e.code
    return JsonResponse(data=data)

@require_GET
@auth_required
def room_info(request):
    room_id = request.GET.get('room_id')
    user = request.user
    room = Room.objects.filter(pk=room_id).first()
    has_apply = False
    if ApplyDetail.objects.filter(user=user.tz_user, room=room):
        has_apply = True
    data = {
        "id": room.id,
        "name": room.name,
        "apply_money": room.apply_money,
        "hot": room.hot,
        "status": room.get_status_display(),
        "pic": room.pic,
        "des": room.des,
        "max_count": room.max_count,
        "current_count": room.current_count,
        "has_apply": has_apply,
    }
    return JsonResponse(data=data)


@require_GET
@auth_required
def banners(request):
    data = []
    banners = Banner.objects.all()
    for _banner in banners:
        data.append({
            'url': _banner.link,
            'img': _banner.pic,
            'title': _banner.des,
        })
    return JsonResponse(data={'data': data})


@require_GET
@auth_required
def apply_history(request):
    data = []
    user = request.user
    detail = ApplyDetail.objects.filter(user=user.tz_user)
    for _d in detail:
        data.append(
            {
                'id': _d.id,
                'room_id': _d.room_id,
                'money': _d.money or 0,
                'create_time':_d.created,
                'max_count':_d.room.max_count,
                'game_name':_d.room.game.name,
                'status':_d.room.get_status_display(),
                'apply_money':_d.room.apply_money,
            }
        )
    return JsonResponse(data={'data': data})


@require_POST
@auth_required
def room_apply(request):
    data = {}
    room_id = request.POST.get('room_id')
    user = request.user.tz_user
    name = request.POST.get('name')
    room = Room.objects.get(pk=room_id)
    a_d = ApplyDetail.objects.filter(user=user, room=room)
    try:
        if a_d:
            raise ApplyAlready()
        if user.card < room.apply_money:
            raise MoneyNotnough()
        user.card = F('card') - room.apply_money
        user.save()
        ApplyDetail.objects.create(
            money=room.apply_money,
            nickname=name,
            user=user,
            room=room,
            status=1,
        )
        room.current_count += 1
        room.save()
        game_password = room.game_password
        Mail.objects.create(
            title='报名成功',
            info='请登录游戏，密码：{game_password}'.format(game_password=game_password),
            user=user
        )
        data = {
            'code': 1,
            'msg': '报名成功'
        }
    except TZBaseError as e:
        data['msg'] = e.msg
        data['code'] = e.code
    # request.GET._mutable = True
    # request.GET['order_id'] = a_d.id
    # request.GET['user_id'] = user_id
    # request.GET._mutable = False
    # res = alipay_info(request)
    # data = {}
    # _data = res.get('data')
    # data['signed_string'] = _data.get('signed_string')
    return JsonResponse(data={'data': data})


def room_apply_balance(request):
    room_id = request.POST.get('room_id')
    user_id = request.POST.get('user_id')
    return JsonResponse(data={'data': []})


def upload_img(request):
    name = hashlib.new('md5', str(request.FILES['file']).encode()).hexdigest()
    handle_upload_file(request.FILES['file'], name)
    return JsonResponse(data={'url': 'http://127.0.0.1/static/uploads/{name}'.format(name=name)})


def handle_upload_file(file, filename):
    path = 'static/uploads/'  # 上传文件的保存路径，可以自己指定任意的路径
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + filename, 'wb+')as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def winner(request):
    room_id = request.POST.get('room_id')
    name = request.POST.get('name')
    img = request.POST.get('img')
    CheckWinner.objects.create(
        room_id=room_id,
        game_user_name=name,
        img=img
    )
    return JsonResponse(data={'code': 1})
