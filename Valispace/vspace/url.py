from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'vspace$', evaluate_input, name='evaluate'),

    url(r'admin$', admin, name='vspaceadmin'),
]