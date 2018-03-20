# # coding:utf-8
import json

import random

import time

from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET

from TZGameServer.middlewares import auth_required
from exception.base import TZBaseError
from exception.room_error import ApplyAlready
from game_room.models import Room, Banner, Game, ApplyDetail
from tz_user.models import TZUser


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


@require_GET
@auth_required
def room_info(request):
    room_id = request.GET.get('room_id')
    user = request.user
    room = Room.objects.filter(pk=room_id).first()
    rank = []
    has_apply = False
    if ApplyDetail.objects.filter(user=user, room=room):
        has_apply = True
    for _rank in room.rank.all():
        rank.append(
            {
                'name': _rank.user.nickname,
                'index': _rank.index
            }
        )
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
        "rank": rank,
    }
    return JsonResponse(data={'data': data})


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
    detail = ApplyDetail.objects.filter(user=user)
    for _d in detail:
        data.append(
            {
                'id':_d.id,
                'room_id':_d.room_id,
                'money': _d.money or 0,
                'value_list': [
                    {
                        'label': '房间名称',
                        'value': _d.room.name
                    },
                    {
                        'label': '房间编号',
                        'value': _d.room.id
                    },

                    {
                        'label': '状态',
                        'value': _d.room.get_status_display()
                    },
                    {
                        'label': '描述',
                        'value': _d.room.des
                    }
                ]
            }
        )
        print(data)
    return JsonResponse(data={'data': data})


@require_POST
@auth_required
def room_apply(request):
    data = {}
    room_id = request.POST.get('room_id')
    user_id = request.POST.get('user_id')
    room = Room.objects.get(pk=room_id)
    user = TZUser.objects.get(pk=user_id)
    a_d = ApplyDetail.objects.filter(user=user)
    try:
        if a_d:
            raise ApplyAlready()
        a_d = ApplyDetail.objects.create(
            money=room.apply_money,
            user=user,
            room=room,
            status=1,
        )
        room.current_count += 1
        room.save()
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
