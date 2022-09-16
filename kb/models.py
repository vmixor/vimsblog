from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class Category(models.Model):
    name = models.CharField('Category name', max_length=32, unique=True)
    description = models.CharField('Description', max_length=255)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Tag(models.Model):
    name = models.CharField('Tag name', max_length=64, unique=True)
    slug = models.SlugField(unique=True)


class Article(models.Model):
    # id_article = models.AutoField()
    title = models.CharField('Article name', max_length=128, unique=True)
    description = models.CharField('Description', max_length=255)
    content = HTMLField()
    is_public = models.BooleanField('Is public', default=False)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField('Creation date and time', auto_now=False, auto_now_add=False)
    publish = models.DateTimeField('Publication date and time', auto_now=False, auto_now_add=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_cat_list(self):
        k = self.category  # for now ignore this instance method
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]
