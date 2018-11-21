# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *
# Register your models here.

class ExpressionAdmin(admin.ModelAdmin):
    list_display=('name', 'description', 'function', 'parameters')


admin.site.register(Expressions, ExpressionAdmin)
