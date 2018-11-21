# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *
from methods import *
from sympy.parsing.sympy_parser import parse_expr
import json

from django.forms import model_to_dict

from django.core.exceptions import ObjectDoesNotExist


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

    return render(request, 'vali.html', {'c': c,})





def admin(request):
    c=locals()
    vars= frommodel()
    fun_json = fun_json_dump(vars['qs'], vars['result_dict'])
    c['frommodel']=vars
    if request.method =='POST':
        print " POST recieved! %s" % request.POST
        if 'action' in request.POST.keys():
            action=request.POST['action']
            myid = request.POST['id']
            obj = Expressions.objects.get(id=myid)
            obj.delete()
            vars = frommodel()
            fun_json = fun_json_dump(vars['qs'], vars['result_dict'])
            return JsonResponse({'fun': fun_json}, safe=True)

        eqn=request.POST.get('eqn', None)
        desc=request.POST.get('desc', None)
        param=request.POST.get('param', None)
        fun= request.POST.get('fun', None)
        print "######################## %s %s %s %s" % (eqn, desc, param, fun)
        try:
            obj=Expressions.objects.get(name=eqn)
            obj_dict= model_to_dict(obj)
            obj_dict['name']=eqn
            obj_dict['description'] = desc
            obj_dict['function'] = fun
            obj_dict['parameters'] =param
            obj=Expressions(**obj_dict)
            obj.save()
        except ObjectDoesNotExist:
            obj=Expressions(
                name=eqn,
                description=desc,
                function=fun,
                parameters=param
            )
            obj.save()
        vars = frommodel()
        fun_json = fun_json_dump(vars['qs'], vars['result_dict'])


        return JsonResponse({'fun':fun_json}, safe=True)
    return render(request, 'admin.html', {'c': c, 'fun':fun_json})


# Create your views here.
