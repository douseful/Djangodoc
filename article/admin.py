from django.contrib import admin

from .models import ArticlePost, ArticleColumn

admin.site.register(ArticleColumn)
admin.site.register(ArticlePost)
