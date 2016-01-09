# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-09 12:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_setting'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='author',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='setting',
            name='blog_title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]