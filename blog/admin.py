from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Tag, Post, Comment


class CategoryAdmin(DraggableMPTTAdmin):
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_public', 'created', 'updated', 'publish')
    list_filter = ('is_public',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'email', 'public', 'created')
    list_filter = ('public',)
    search_fields = ['name', 'email', 'content']


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)
