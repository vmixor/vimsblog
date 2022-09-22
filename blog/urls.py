from django.urls import path, re_path
from . import views


urlpatterns = [
    # url(r'^category/(?P<hierarchy>.+)/$', views.show_category, name='category'),
    re_path('^$', views.index, name='index'),
    re_path('^category/(?P<hierarchy>.+)/$', views.show_category, name='category'),
]
