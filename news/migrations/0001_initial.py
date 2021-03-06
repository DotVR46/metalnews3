# Generated by Django 3.2 on 2021-04-25 13:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import news.models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('duration', models.DurationField(blank=True, verbose_name='Длительность')),
                ('release_date', models.DateField(blank=True, verbose_name='Дата релиза')),
                ('cover', models.ImageField(upload_to=news.models.get_covers_upload_path, verbose_name='Обложка')),
                ('slug', models.SlugField(blank=True, max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Альбом',
                'verbose_name_plural': 'Альбомы',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='MusicLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('description', models.CharField(max_length=500, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Лейбл',
                'verbose_name_plural': 'Лейблы',
            },
        ),
        migrations.CreateModel(
            name='MusicStyle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('slug', models.SlugField(blank=True, max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Музыкальный стиль',
                'verbose_name_plural': 'Музыкальные стили',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=5000, verbose_name='Сообщение')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.album', verbose_name='Альбом')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.review', verbose_name='Родитель')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200, verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='Содержание')),
                ('image', models.ImageField(blank=True, upload_to='posts/%Y%m%d/')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('views', models.PositiveIntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('category', models.ManyToManyField(blank=True, related_name='post_categories', to='news.Category', verbose_name='Категории')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ('-publish',),
            },
        ),
        migrations.CreateModel(
            name='LikeDislike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.SmallIntegerField(choices=[(-1, 'Не коза'), (1, 'Коза')], verbose_name='Голос')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('text', models.TextField(max_length=5000, verbose_name='Сообщение')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.comment', verbose_name='Родитель')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post', verbose_name='Новость')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(upload_to=news.models.get_band_upload_path, verbose_name='Фото')),
                ('country', models.CharField(max_length=100, verbose_name='Страна')),
                ('slug', models.SlugField(blank=True, max_length=200)),
                ('styles', models.ManyToManyField(related_name='band_style', to='news.MusicStyle', verbose_name='Стили/Жанры')),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
            },
        ),
        migrations.AddField(
            model_name='album',
            name='band',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.band', verbose_name='Группа/Исполнитель'),
        ),
        migrations.AddField(
            model_name='album',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.musiclabel', verbose_name='Лейбл'),
        ),
        migrations.AddField(
            model_name='album',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
