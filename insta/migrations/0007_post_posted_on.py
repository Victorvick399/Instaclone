# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-01-05 13:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0006_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='posted_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
