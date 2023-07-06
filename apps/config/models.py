from django.db import models
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
# Create your models here.
from django.db import models
# Create your models here.

class Link(models.Model):
    STATUS_CHOICES = (
        (1, '正常'),
        (0, '删除')
    )
    title = models.CharField(max_length=100, verbose_name='标题')
    href = models.URLField(verbose_name='链接')
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=1, verbose_name='状态')
    weight = models.PositiveIntegerField(default=1,choices=zip(range(1,6),range(1,6)),verbose_name='权重')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    class Meta:
        db_table='df_link'
        verbose_name='权重'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.title

class SideBar(models.Model):
    # 侧边栏显示界面，在这里显示最近的新鲜文章
    STATUS_CHOICES = (
        (1, '显示'),
        (0, '隐藏'),
    )
    display_html=0
    display_latset=1
    display_hot=2
    display_comment=3
    TYPE_CHOICES = (
        (display_html, 'HTML'),
        (display_latset, '最新文章'),
        (display_hot, '最热文章'),
        (display_comment, '最热评论'),
    )
    title = models.CharField(max_length=100, verbose_name='标题')
    tpye = models.IntegerField(choices=TYPE_CHOICES,default=1,verbose_name='展示类型')
    content = models.CharField(max_length=400,blank=True,verbose_name='内容')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES,default=1,verbose_name='显示状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table='df_sidebar'
        verbose_name='侧边栏'
        verbose_name_plural=verbose_name
    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=1)

    @property
    #添加了property之后可以用属性来调用方法
    def content_html(self):
        from apps.blog.models import Post
        from apps.comment.models import Comment

        result=''
        if self.tpye==self.display_html:
            result=self.content

        elif self.tpye==self.display_latset:
            context={
                'posts':Post.latest_posts()
            }

            result=render_to_string('config/sidebar_posts.html',context)
        elif self.tpye==self.display_hot:
            context = {
                'posts': Post.host_posts()
            }
            result = render_to_string('config/sidebar_posts.html', context)

        elif self.tpye==self.display_comment:
            context={
                'comments':Comment.objects.filter(status=1)
            }
            result=render_to_string('config/blocks/sidebar_comments.html',context)

        return result



