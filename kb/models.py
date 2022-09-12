from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


# Create your models here.
class Category(models.Model):
    name = models.CharField('Category name', max_length=64)
    description = models.CharField('Description', max_length=255)
    slug = models.SlugField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)


class Tag(models.Model):
    name = models.CharField('Tag name', max_length=64)
    slug = models.SlugField()


class Article(models.Model):
    # id_article = models.AutoField()
    name = models.CharField('Article name', max_length=128)
    description = models.CharField('Description', max_length=255)
    content = HTMLField()
    is_public = models.BooleanField('Is public', default=False)
    created = models.DateTimeField('Creation date and time')
    slug = models.SlugField()
    publish = models.DateField(auto_now=False, auto_now_add=False,)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
