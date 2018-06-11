# coding=utf-8
# Created by TTc9082 on 12/16/14
import json

from datetime import datetime
from django import forms
from exception.room_error import *
from game_room.models import Room, Game


#
class CreateRoomForm(forms.Form):
    name = forms.CharField(required=False)
    apply_money = forms.IntegerField(required=False)
    des = forms.CharField(required=False)
    max_count = forms.IntegerField(required=False)
    game = forms.IntegerField(required=False)
    start_time = forms.CharField(required=False)
    end_time = forms.CharField(required=False)
    game_password = forms.CharField(required=False)

    class Meta:
        model = Room
        fields = ['name', 'apply_money', 'des', 'max_count', 'game', 'start_time', 'end_time', 'game_password']

    def clean_name(self):
        if not self.cleaned_data['name']:
            raise NameRequire()
        return self.cleaned_data['name']
    def clean_apply_money(self):
        if not self.cleaned_data['apply_money']:
            raise NameRequire()
        return int(self.cleaned_data['apply_money'])

    def clean_des(self):
        if not self.cleaned_data['des']:
            raise DescRequire()
        return self.cleaned_data['des']

    def clean_max_count(self):
        if not self.cleaned_data['max_count']:
            raise MaxCountRequire()
        return int(self.cleaned_data['max_count'])

    def clean_game(self):
        if not self.cleaned_data['game']:
            raise GameRequire()

        game = Game.objects.filter(id=self.cleaned_data['game']).first()
        if not game:
            raise GameDoesNotExist()
        return game


    def clean_start_time(self):
        if not self.cleaned_data['start_time']:
            raise NameRequire()
        day = self.cleaned_data['start_time'].split(',')[0]
        hour = self.cleaned_data['start_time'].split(',')[1]
        minute = self.cleaned_data['start_time'].split(',')[2]
        _time = f'{day} {hour}:{minute}'
        self.start_time = datetime.strptime(_time, '%Y-%m-%d %H:%M')
        return self.start_time

    def clean_end_time(self):
        if not self.cleaned_data['end_time']:
            raise NameRequire()

        day = self.cleaned_data['end_time'].split(',')[0]
        hour = self.cleaned_data['end_time'].split(',')[1]
        minute = self.cleaned_data['end_time'].split(',')[2]
        _time = f'{day} {hour}:{minute}'
        self.end_time = datetime.strptime(_time, '%Y-%m-%d %H:%M')
        if self.end_time <= self.start_time:
            raise EndMustBiggerStart()
        return self.end_time

    def save(self):
        if self.cleaned_data['game'].id == 1:
            self.cleaned_data['pic'] = 'http://pic.616pic.com/bg_w1180/00/03/32/iNYXcaFHC1.jpg!/fw/1120'
        else:
            self.cleaned_data['pic'] = 'http://static.588ku.com/imgPath/comboVip/images/cp-banner.jpg'

        room = Room.objects.create(
            **self.cleaned_data
        )
        return room