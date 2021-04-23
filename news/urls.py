from django.urls import path
from .views import *

app_name = 'news'

urlpatterns = [
    path('', MainPage.as_view(), name='post_list'),
    path('<str:slug>/', post_detail, name='post_detail'),
    path('comment/<str:slug>/', AddComment.as_view(), name='add_comment'),
]