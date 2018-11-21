# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "valispace.settings")

django.setup()
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from sympy.solvers.solveset import linsolve
from vspace.models import *
from django.core import serializers
from django.utils.safestring import mark_safe
import json




def frommodel():
    """This method queries the  Expression model class and tries to solve them
        together using linear algebra method where possible, otherwise,
        it simply evaluates where expression is more of a function... in this case

        """

    # f1, f2, f3, f4, f5 = symbols('f1, f2, f3, f4, f5')
    # query
    qs = Expressions.objects.all()
    values = ['name', 'function']
    # create list of dicts from containing only name and function fields
    values_list = qs.values(*values)

    # define a fe variables to use in the latter
    eqn_array, var_list_obj, var_list_str, mul_exp = [], [], [], []
    result_dict = {}

    for i, d in enumerate(values_list):
        # parse functions to make real expression from the strings
        var1 = parse_expr(d['name'])
        exprs = parse_expr(d['function'])
        # multiply right hand side by -1
        exprs_inv = exprs * -1

        # check if function is the multiplication function to treat differently after
        if 'Mul' in str(exprs.func):
            totexp = var1 + (exprs_inv)
            mul_exp.append(d)
        # add the left and right nad side togther and append to a list
        totexp = var1 + exprs_inv
        eqn_array.append(totexp)

        # list sympy object, and string of the name field to a list to use latter

        var_list_obj.append(var1)
        var_list_str.append(d['name'])
    # evaluate together as linear algebra
    result = linsolve(eqn_array, var_list_obj)
    # create dictionary for the result for easy access going forward
    for l in result:
        for i, j in enumerate(var_list_str):
            r_d = {j: l[i]}
            result_dict.update(r_d)
    # Evaluate multiplication expression and update the result dict with new value
    for item in mul_exp:
        sub = {}
        excp_var = parse_expr(item['function']).free_symbols
        for y in excp_var:
            try:
                kv = {str(y): result_dict[str(y)]}
                print item
                sub.update(kv)
            except Exception as e:
                print"str(item) was not previously known +%s" % e
            calc = parse_expr(str(item['function'])).subs(sub)
            result_dict.update({str(item['name']): calc})
    # return all local variables for easy access in other functions
    return locals()


def eval(strinput):
    """Function evaluates the result of a given string input based on the
       previously calculated values. Calls the function 'frommodel()' also uses
       variables defined in that function
    """
    # convert string input to and expression
    eqn = parse_expr(strinput)
    # derive all varibles in the expression
    vars = eqn.free_symbols
    # call the frommodel() functions to introduce variables from it into this functions
    solutions = frommodel()
    sub_dict = {}
    # retrieve corresponding values of variables from based on calculation made in 'frommodel()'
    for item in vars:
        try:
            kv = {str(item): solutions['result_dict'][str(item)]}
            sub_dict.update(kv)
        except Exception as e:
            print"str(item) was not previously known"

    # evaluate
    calc = eqn.subs(sub_dict)

    return calc


def fun_json_dump(qs, result_dict):
    fun_serialized = serializers.serialize('python', qs)
    for item in fun_serialized:
        name = item['fields']['name']
        try:
            item['fields']['current_value'] = str(result_dict[name])
        except Exception as e:
            item['fields']['current_value'] = 'Cannot be evaluted'

    fun_json = mark_safe(json.dumps(fun_serialized))
    return fun_json