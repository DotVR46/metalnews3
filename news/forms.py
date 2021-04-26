from django import forms

from news.models import Comment, Review


class CommentForm(forms.ModelForm):
    """Форма комментов"""

    class Meta:
        model = Comment
        fields = ('name', 'email', 'text')


class ReviewForm(forms.ModelForm):
    """Форма комментов"""

    class Meta:
        model = Review
        fields = ('text',)
