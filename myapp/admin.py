from django.contrib import admin
from .models import *
# Register your models here.

class AccountAdmin(admin.ModelAdmin):
  list_display = ['user']

admin.site.register(Account, AccountAdmin)

class PostAdmin(admin.ModelAdmin):
  list_display = ['id','user_id','created_at']

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
  list_display = ['id','text']

admin.site.register(Comment, CommentAdmin)

admin.site.register(Like)

admin.site.register(Follower)
