from django import forms
from django.contrib import admin
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Post


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(label='Содержание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


admin.site.register(Post, PostAdmin)
admin.site.register(Band)
admin.site.register(Album)
admin.site.register(Review)
admin.site.register(MusicStyle)
admin.site.register(MusicLabel)
# admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)

admin.site.site_title = 'Metalnews'
admin.site.site_header = 'Metalnews'
