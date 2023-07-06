from django.contrib import admin
from apps.comment.models import Comment
from django.contrib.auth.models import User
# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('body','nick_name','created','status','article')
