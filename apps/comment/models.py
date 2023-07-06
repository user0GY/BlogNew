from django.db import models
from django.db import models
from django.contrib.auth.models import User
from apps.blog.models import Post

# Create your models here.
class Comment(models.Model):
    STATUS_CHOICES = (
        (1, '正常'),
        (0, '删除')
    )
    article = models.ForeignKey(Post,on_delete=models.CASCADE, verbose_name= 'comments')
    body = models.TextField(verbose_name='内容')
    nick_name = models.CharField(max_length=16, verbose_name='昵称')
    email = models.EmailField(verbose_name='邮箱')
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=1, verbose_name='状态')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'df_comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name