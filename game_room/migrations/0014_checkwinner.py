# Generated by Django 2.0.2 on 2018-04-24 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_room', '0013_auto_20180422_1141'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckWinner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.IntegerField(choices=[(0, 'NO'), (1, 'YES')], default=0, verbose_name='是否删除')),
                ('room_id', models.IntegerField(verbose_name='房间ID')),
                ('game_user_name', models.CharField(max_length=32, verbose_name='游戏昵称')),
                ('img', models.CharField(max_length=512, verbose_name='状态')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
    ]
