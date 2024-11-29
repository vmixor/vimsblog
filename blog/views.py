from django.shortcuts import get_object_or_404
from django.views import generic
from django.utils import timezone
from .models import Post, Category, Comment
from .forms import CommentForm


class PostList(generic.ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 5

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if 'hierarchy' in self.kwargs:
            # Split the category hierarchy into parts
            slu = self.kwargs['hierarchy'].split('/')
            slug = slu[-1] if slu[-1] != '' else slu[-2]
            # Load main category
            category = get_object_or_404(Category, slug=slug)
            # Load all subcategories
            descendant_categories = category.get_descendants(include_self=True)
            # Filter articles by category and its descendants
            return qs.filter(
                category__in=descendant_categories,
                is_public=True,
                publish__lte=timezone.now()
            ).order_by('-publish')
        else:
            return qs.filter(is_public=True, publish__lte=timezone.now()).order_by('-publish')

    # Add categories records for category list (in base.html)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs["slug"]

        form = CommentForm()
        post = get_object_or_404(Post, slug=slug)
        categories = Category.objects.all()  # get all categories
        comments = post.comments.filter(public=True)

        context['categories'] = categories
        context['comments'] = comments
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post = Post.objects.filter(slug=self.kwargs['slug'])[0]
        comments = post.comments.filter(public=True)
        categories = Category.objects.all()  # get all categories

        context['post'] = post
        context['categories'] = categories
        context['comments'] = comments
        context['form'] = form

        if form.is_valid() and post.add_comments:
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']

            comment = Comment.objects.create(
                name=name, email=email, content=content, post=post
            )

            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)


class About(generic.TemplateView):
    template_name = 'blog/about.html'

    # Add categories records for category list (in base.html)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
