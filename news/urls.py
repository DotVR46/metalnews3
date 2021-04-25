from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *

app_name = 'news'

urlpatterns = [
    path('', MainPage.as_view(), name='post_list'),
    path('<str:slug>/', post_detail, name='post_detail'),
    path('comment/<str:slug>/', AddComment.as_view(), name='add_comment'),
    path('category/<str:category_name>', CategoryListView.as_view(), name='category_post_list'),
    path('post/<int:pk>/like/',
         login_required(VotesView.as_view(model=Post, vote_type=LikeDislike.LIKE)),
         name='post_like'),
    path('post/<int:pk>/dislike/',
         login_required(VotesView.as_view(model=Post, vote_type=LikeDislike.DISLIKE)),
         name='post_dislike'),
    path('comment/<int:pk>/like/',
         login_required(VotesView.as_view(model=Comment, vote_type=LikeDislike.LIKE)),
         name='comment_like'),
    path('comment/<int:pk>/dislike/',
         login_required(VotesView.as_view(model=Comment, vote_type=LikeDislike.DISLIKE)),
         name='comment_dislike'),
]
