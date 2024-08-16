from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'author')
    list_filter = ('author', 'type')
    search_fields = ('title', 'type')


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'post')
    list_filter = ('category', 'post')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_title', 'rating')
    list_filter = ('user',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
