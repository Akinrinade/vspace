# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-17 00:49
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expressions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Please check', regex='^[#](\\w+)$')])),
                ('description', models.TextField(help_text='Provide a breief but detailed decription of this function: Note max 200 characters')),
                ('function', models.CharField(max_length=50)),
                ('parameters', models.CharField(help_text='Please enter parameter list seperated by comma', max_length=50)),
            ],
            options={
                'verbose_name': 'Expression',
                'verbose_name_plural': 'Expressions',
            },
        ),
    ]
