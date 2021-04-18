from django.urls import path
from .views import *

app_name = 'news'

urlpatterns = [
    path('', post_list, name='post_list')
]