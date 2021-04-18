from django.shortcuts import render

# Create your views here.
from news.models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'news/post_list.html', context)