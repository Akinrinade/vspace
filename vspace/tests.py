# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time


from .models import *
from django.test import LiveServerTestCase, Client, TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


# Create your tests here.
class ExpressionsModelTests(TestCase):
    client = Client()



    def test_expression_creation(self):
        """test the ability to create instance of Epression"""
        # exp = Expressions(name='f0', function='f3+f4', description='test', parameters='f3, f4')

        Expressions.objects.create(
            name='f0',
            function='f3+f4',
            description='test',
            parameters='f3, f4'
            )

        self.assertIsInstance(Expressions.objects.get(name='f0', function='f3+f4',
        description='test', parameters='f3, f4'), Expressions, 'Object created successfully')



    def test_expression_name(self):
        """test to ensure the model name complies with the given
        expression
        """
        # create model instance with non-complying name
        exp=Expressions(
            name='..+',
            function='f3+f4',
            description ='test',
            parameters='f3, f4')

        self .assertRaises(RegexValidator, exp.full_clean())

    def test_basic_view(self):
        response = self.client.get('/vspace/')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):

        exp = Expressions.objects.all()

        exp.delete()



# more testing

class evaluate_inputTestCase(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(evaluate_inputTestCase, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(evaluate_inputTestCase, cls).tearDownClass()


    def test_register(self):
        selenium = self.selenium

        # Open vspace page

        selenium.get('http://localhost:8080/vspace/')

        # get find the form element
        eqn = selenium.find_element_by_id('eqn')
        submit = selenium.find_element_by_id('evaluate')

        # Fill the form with data
        eqn.send_keys('f1+f2')

        # submit
        submit.send_keys(Keys.RETURN)

        #wait 5 seconds
        time.sleep(5)
        # search for result element and get text value
        result = selenium.find_element_by_id('result')

        answer = result.text

        print "##############Result = %s" % answer

        # check the returned result
        self.assertEqual(int(answer), 87, 'result  is %s and to %s' % (answer, 87))