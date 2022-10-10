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
            slu = self.kwargs['hierarchy'].split('/')
            slug = slu[-1] if slu[-1] != '' else slu[-2]
            category = Category.objects.filter(slug=slug).first()
            return qs.filter(category=category)
        else:
            return qs


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


def show_category(request, hierarchy=None):
    category_slug = hierarchy.split('/')
    category_queryset = list(Category.objects.all())
    all_slugs = [x.slug for x in category_queryset]
    parent = None
    for slug in category_slug:
        if slug in all_slugs:
            parent = get_object_or_404(Category, slug=slug, parent=parent)
        else:
            instance = get_object_or_404(Post, slug=slug)
            breadcrumbs_link = instance.get_cat_list()
            category_name = [' '.join(i.split('/')[-1].split('-')) for i in breadcrumbs_link]
            breadcrumbs = zip(breadcrumbs_link, category_name)
            return render(request, "postDetail.html", {'instance': instance, 'breadcrumbs': breadcrumbs})

    return render(request, "blog/categories.html",
                  {'article_set': parent.post_set.all(), 'sub_categories': parent.children.all()})
