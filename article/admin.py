from django.contrib import admin

from .models import *

@admin.register(Article)
class ArticleModel(admin.ModelAdmin):
    list_display = ('title', 'category', 'color_state')
    list_per_page = 30
    date_hierarchy = 'pub_date'
    search_fields = ('title',)
    
    admin.site.site_header = '文章发布系统'
    admin.site.site_title = '文章发布'
    
        

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'last_updated')
    list_per_page = 30

@admin.register(ArticleComment)
class ArticleCommentAdmin(admin.ModelAdmin):
        list_display = ('id', 'article', 'state', 'pub_time')
        list_per_page = 50

