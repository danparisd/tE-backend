# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 20:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20170627_1651'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='project',
            new_name='language',
        ),
    ]