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

from exception.base import TZBaseError
from game_room.models import Room, Banner, Game
from tz_user.forms import SignUpForm
import hashlib
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
    room_id = request.GET.get('room_id')
    room = Room.objects.get(room=room_id)
    data = {
        'id': room.id,
        'name': room.name,
        'apply_money': room.apply_money,
        'pic': room.pic,
        'max_count': room.max_count,
        'current_count': room.current_count,
        'apply': room.apply,
        'game': room.game,
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

def apply(request):
    """
    报名 支付宝回调
    :param request:
    :return:
    """
    pass