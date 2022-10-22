from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post, Category
from django.utils import timezone


class PostList(generic.ListView):
    queryset = Post.objects.filter(is_public=True, publish__lte=timezone.now()).order_by('-publish')
    template_name = 'blog/index.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if 'hierarchy' in self.kwargs:
            slu = self.kwargs['hierarchy'].split('/')  # split category hierarchy url string into list
            slug = slu[-1] if slu[-1] != '' else slu[-2]  # get last non-empty slug element
            category = Category.objects.filter(slug=slug).first()  # get first() element from list
            return qs.filter(category=category)  # filter Posts by category
        else:
            return qs

    # Add categories records for category list (in base.html)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    # Add categories records for category list (in base.html)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
