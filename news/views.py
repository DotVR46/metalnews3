import json

from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic.base import View
from django.contrib.contenttypes.models import ContentType
# Create your views here.
from news.models import Post, Category, Album, Comment, LikeDislike
from .forms import CommentForm


class MainPage(ListView):
    model = Post
    template_name = 'news/post_list.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p = Paginator(Post.objects.select_related().all(), self.paginate_by)
        context['posts'] = p.page(context['page_obj'].number)
        context['categories'] = Category.objects.all()
        context['albums'] = Album.objects.all()
        context['comments'] = Comment.objects.all().order_by('-created')[:3]
        context['popular_day'] = Post.objects.all().filter(
            publish__range=[timezone.now() - timezone.timedelta(days=1), timezone.now()]).annotate(
            sum_views=Sum('views'), sum_votes=Sum('votes')).order_by('-sum_views', 'sum_votes')[:3]
        context['popular_week'] = Post.objects.all().filter(
            publish__range=[timezone.now() - timezone.timedelta(days=7), timezone.now()]).annotate(
            sum_views=Sum('views'), sum_votes=Sum('votes')).order_by('-sum_views', 'sum_votes')[:3]
        context['popular_month'] = Post.objects.all().filter(
            publish__range=[timezone.now() - timezone.timedelta(days=30), timezone.now()]).annotate(
            sum_views=Sum('views'), sum_votes=Sum('votes')).order_by('-sum_views', 'sum_votes')[:3]
        context['popular_years'] = Post.objects.all().annotate(
            sum_views=Sum('views'), sum_votes=Sum('votes')).order_by('-sum_views', 'sum_votes')[:3]
        return context


class CategoryListView(ListView):
    model = Post
    template_name = 'news/category_post_list.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p = Paginator(Post.objects.select_related().filter(category__name=self.kwargs.get('category_name')), self.paginate_by)
        context['posts'] = p.page(context['page_obj'].number)
        context['comments'] = Comment.objects.all().order_by('-created')[:3]
        context['popular_day'] = Post.objects.all().filter(
            publish__range=[timezone.now() - timezone.timedelta(days=1), timezone.now()]).annotate(
            sum_views=Sum('views'), sum_votes=Sum('votes')).order_by('-sum_views', 'sum_votes')[:3]
        context['popular_week'] = Post.objects.all().filter(
            publish__range=[timezone.now() - timezone.timedelta(days=7), timezone.now()]).annotate(
            sum_views=Sum('views'), sum_votes=Sum('votes')).order_by('-sum_views', 'sum_votes')[:3]
        context['popular_month'] = Post.objects.all().filter(
            publish__range=[timezone.now() - timezone.timedelta(days=30), timezone.now()]).annotate(
            sum_views=Sum('views'), sum_votes=Sum('votes')).order_by('-sum_views', 'sum_votes')[:3]
        context['popular_years'] = Post.objects.all().annotate(
            sum_views=Sum('views'), sum_votes=Sum('votes')).order_by('-sum_views', 'sum_votes')[:3]
        return context


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.views += 1
    post.save(update_fields=['views'])
    context = {
        'post': post,
    }
    return render(request, 'news/post_detail.html', context)


class AddComment(View):
    """Комментарии"""

    def post(self, request, slug):
        form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.post = post
            form.save()
        return redirect(post.get_absolute_url())


class VotesView(View):
    model = None  # Модель данных - Статьи или Комментарии
    vote_type = None  # Тип комментария Like/Dislike

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        # GenericForeignKey не поддерживает метод get_or_create
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                                  user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )
