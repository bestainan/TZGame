# Generated by Django 2.0.2 on 2018-04-24 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_room', '0016_auto_20180424_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='des',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='描述'),
        ),
        migrations.AddField(
            model_name='room',
            name='max_count',
            field=models.IntegerField(default=0, verbose_name='最大人数'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='pic',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='图片地址'),
        ),
    ]