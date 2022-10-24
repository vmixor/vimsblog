from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse


class Category(MPTTModel):
    name = models.CharField('Category name', max_length=32, unique=True)
    description = models.TextField('Description')
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def get_absolute_url(self):
        full_path = [self.slug]
        k = self.parent
        while k is not None:
            full_path.append(k.slug)
            k = k.parent
        return reverse('category', args=[str('/'.join(full_path[::-1]))])


class Tag(models.Model):
    name = models.CharField('Tag name', max_length=32, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField('Title', max_length=128, unique=True)
    description = models.TextField('Description')
    content = HTMLField()
    is_public = models.BooleanField('Is public', default=False)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField('Creation date and time', auto_now_add=True)
    updated = models.DateTimeField('Last modification date and time', auto_now=True)
    publish = models.DateTimeField('Publication date and time', auto_now=False, auto_now_add=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def get_cat_list(self):
        k = self.category  # for now ignore this instance method
        breadcrumb = ['dummy']
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]
