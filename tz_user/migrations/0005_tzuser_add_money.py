# Generated by Django 2.0.2 on 2018-06-12 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tz_user', '0004_tzuser_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='tzuser',
            name='add_money',
            field=models.IntegerField(default=0, verbose_name='加钱'),
        ),
    ]
