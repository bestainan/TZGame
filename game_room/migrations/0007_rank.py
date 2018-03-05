# Generated by Django 2.0.2 on 2018-03-03 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tz_user', '0002_auto_20180303_0720'),
        ('game_room', '0006_auto_20180303_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.IntegerField(choices=[(0, 'NO'), (1, 'YES')], default=0, verbose_name='是否删除')),
                ('index', models.IntegerField(verbose_name='排名')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rank', to='game_room.Room')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tz_user.TZUser')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
    ]
