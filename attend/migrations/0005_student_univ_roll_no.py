# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-03 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attend', '0004_student_add_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='univ_roll_no',
            field=models.CharField(default='University Roll No.', max_length=10),
        ),
    ]