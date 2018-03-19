# # coding:utf-8
import json

import random

import time

from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from alipay.views import alipay_info
from game_room.models import Room, Banner, Game, ApplyDetail
from tz_user.models import TZUser


@require_GET
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
def room_info(request):
    room_id = request.GET.get('room_id')
    room = Room.objects.filter(pk=room_id).first()
    rank = []
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
        "rank": rank,
    }
    return JsonResponse(data={'data': data})


@require_GET
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
def apply_history(request):
    data = []
    user_id = request.GET.get('user_id')
    detail = ApplyDetail.objects.filter(user=user_id)
    for _d in detail:
        data.append(
            [{

                'money': _d.money,
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
            }]
        )
    return JsonResponse(data={'data': data})


@require_POST
def room_apply(request):
    room_id = request.POST.get('room_id')
    user_id = request.POST.get('user_id')
    room = Room.objects.get(pk=room_id)
    user = TZUser.objects.get(pk=user_id)
    a_d = ApplyDetail.objects.create(
        money = room.apply_money,
        user=user,
        room=room
    )
    request.GET._mutable = True
    request.GET['order_id'] = a_d.id
    request.GET['user_id'] = user_id
    request.GET._mutable = False
    res = alipay_info(request)
    data = {}
    _data = res.get('data')
    data['signed_string'] = _data.get('signed_string')
    return JsonResponse(data={'data': data})

def room_apply_balance(request):
    room_id = request.POST.get('room_id')
    user_id = request.POST.get('user_id')
    return JsonResponse(data={'data': []})
