# Generated by Django 2.0.2 on 2018-03-04 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_room', '0008_auto_20180304_0447'),
    ]

    operations = [
        migrations.AddField(
            model_name='applydetail',
            name='status',
            field=models.IntegerField(choices=[(0, '已完成'), (1, '待支付'), (2, '支付中'), (3, '支付失败')], default=1, verbose_name='状态'),
        ),
    ]
