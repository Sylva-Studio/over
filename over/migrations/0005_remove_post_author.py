# Generated by Django 3.1.3 on 2020-11-18 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('over', '0004_auto_20201118_1612'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
    ]
