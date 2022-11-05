from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    re_path('^category/(?P<hierarchy>.+)$', views.PostList.as_view(), name='category'),
    path('detail/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('about/', views.About.as_view(), name='about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
