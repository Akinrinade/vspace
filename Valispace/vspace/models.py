# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator
# Create your models here.


class Expressions(models.Model):

    """"Model class for the different expressions"""

    name = models.CharField(max_length = 50, validators=[
            RegexValidator(regex='([\w\-_]+)', message='Please check the name entry',), ],)
    description = models.TextField(help_text=
                'Provide a breief but detailed decription of this function:'
                ' Note max 200 characters')
    function = models.CharField(max_length = 50,)
    parameters=models.CharField(max_length=50, help_text=
            'Please enter parameter list seperated by comma')


    @property
    def variable_list(self):
        return self.parameters.split(',')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name='Expression'
        verbose_name_plural='Expressions'
