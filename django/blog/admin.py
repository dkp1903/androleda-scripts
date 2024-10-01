from django.contrib import admin
from .models import Blog, Tag, BlogCategory

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'category')
    search_fields = ('title', 'summary')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
