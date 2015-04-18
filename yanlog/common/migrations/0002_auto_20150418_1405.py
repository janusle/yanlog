# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='github',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='setting',
            name='linkedin',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='setting',
            name='twitter',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='setting',
            name='avatar',
            field=models.ImageField(null=True, upload_to=b'', blank=True),
        ),
    ]
