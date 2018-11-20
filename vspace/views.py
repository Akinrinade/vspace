# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *
from methods import *
from sympy.parsing.sympy_parser import parse_expr
import json
from django.core import serializers


def evaluate_input(request):
    c=locals()
    c['frommodel'] = frommodel()

    if request.method =='POST':
        print " POST recieved! %s" % request.POST
        eqn=request.POST['eqn']
        # eqn=parse_expr(eqn)
        # vars = eqn.free_symbols
        # vars= json.loads(vars)
        soln = eval(eqn)
        print "Here out soln %s" %soln
        return JsonResponse(json.dumps({'soln': str(soln)}), safe=False)

    return render(request, 'valibase.html', {'c': c,})

# Create your views here.
