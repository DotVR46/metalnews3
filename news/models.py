from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


def get_covers_upload_path(instance, filename):
    return f'covers/{instance.band.name}/{instance.name}/{filename}'


def get_band_upload_path(instance, filename):
    return f'band/{instance.name}/{filename}'


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('tag-detail-url', kwargs={'slug': self.slug})
    #
    # def get_update_url(self):
    #     return reverse('tag-update-url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Post(models.Model):
    """Новость на сайте"""
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField('Заголовок', max_length=200, db_index=True)
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='posts/%Y%m%d/', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    slug = models.SlugField(max_length=200, blank=True, unique=True)
    tags = models.ManyToManyField(Tag, verbose_name='Теги', blank=True, related_name='post_tags')

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


# class User(models.Model):
#     """Пользователь"""
#     pass


# class Comment(models.Model):
#     """Комментарии к постам"""
#     pass


class MusicStyle(models.Model):
    """Музыкальный стиль"""
    name = models.CharField('Название', max_length=100, db_index=True)
    description = models.TextField('Описание')
    slug = models.SlugField(max_length=160, blank=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(MusicStyle, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Музыкальный стиль'
        verbose_name_plural = 'Музыкальные стили'


class Band(models.Model):
    """Группа/Исполнитель"""

    name = models.CharField('Название', max_length=200)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Фото', upload_to=get_band_upload_path)
    country = models.CharField('Страна', max_length=100)
    styles = models.ManyToManyField(MusicStyle, verbose_name='Стили/Жанры',
                                    related_name='band_style')
    slug = models.SlugField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Band, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class MusicLabel(models.Model):
    """Лейбл/Студия"""
    name = models.CharField('Название', max_length=150)
    description = models.CharField('Описание', max_length=500)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Лейбл'
        verbose_name_plural = 'Лейблы'


class Album(models.Model):
    """Альбом"""
    name = models.CharField('Название', max_length=200, db_index=True)
    description = models.TextField(verbose_name='Описание')
    duration = models.DurationField('Длительность', blank=True)
    release_date = models.DateField('Дата релиза', blank=True)
    band = models.ForeignKey(Band, verbose_name='Группа/Исполнитель', on_delete=models.CASCADE)
    label = models.ForeignKey(MusicLabel, verbose_name='Лейбл', on_delete=models.CASCADE)
    cover = models.ImageField(verbose_name='Обложка', upload_to=get_covers_upload_path)
    slug = models.SlugField(max_length=160, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name + '-' + self.band.name)
        super(Album, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.band.name} - {self.name} {self.release_date.year}'

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'


class Review(models.Model):
    """Обзор альбома"""
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    text = models.TextField('Сообщение', max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True
    )
    album = models.ForeignKey(Album, verbose_name='Альбом', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.album.name}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
