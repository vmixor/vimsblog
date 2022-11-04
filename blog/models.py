from django.db import models
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse

User = get_user_model()


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
    add_comments = models.BooleanField('Add new comments', default=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField('Nick', max_length=32)
    email = models.EmailField('E-mail', max_length=64)
    content = models.TextField('Content')
    public = models.BooleanField('Is public', default=False)
    created = models.DateTimeField('Creation date and time', auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name
