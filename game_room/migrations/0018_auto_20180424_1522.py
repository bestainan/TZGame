# Generated by Django 2.0.2 on 2018-04-24 15:22

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('game_room', '0017_auto_20180424_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='current_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='当前人数'),
        ),
        migrations.AddField(
            model_name='room',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 24, 15, 22, 34, 731737, tzinfo=utc), verbose_name='结束报名时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='game_room.Game'),
        ),
        migrations.AddField(
            model_name='room',
            name='game_password',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='图片地址'),
        ),
        migrations.AddField(
            model_name='room',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 24, 15, 22, 39, 532330, tzinfo=utc), verbose_name='开始报名时间'),
            preserve_default=False,
        ),
    ]