from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created_at', 'updated_at', 'user')

admin.site.register(BlogPost, BlogPostAdmin)

class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'blog','created_at', 'updated_at', 'user')

admin.site.register(BlogComment, BlogCommentAdmin)
