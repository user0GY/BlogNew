from django.db import models
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.urls import reverse
from django.utils import timezone
# Create your models here.
from django.db import models
# Create your models here.


class BaseModel(models.Model):
    STATUS_CHOICES = (
        (1, '正常'),
        (0, '删除')
    )
    name = models.CharField(max_length=32, verbose_name='名称')
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=1, verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class Category(BaseModel):
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航标签')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    class Meta:
        db_table = 'df_catefory'
        verbose_name = "分类"
        verbose_name_plural = verbose_name
    #添加了这个方法之后查看文章就不是objects而是名字了
    def __str__(self):
        return self.name


class Tag(BaseModel):
    # 标签模型
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    class Meta:
        db_table = 'df_Tag'
        verbose_name = '标签'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = (
        (1, '正常'),
        (0, '删除'),
        (2, '草稿'),
    )

    # 文章标题,models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100, verbose_name='标题')
    # 文章摘要
    content = models.CharField(max_length=100, verbose_name='摘要')
    # 文章作者
    author = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)
    # 文章正文,保存大量文本使用 TextField
    body = models.TextField(help_text='正文需为MarkDown格式', verbose_name='正文')
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=1, verbose_name='状态')
    # 文章创建时间,参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created_time = models.DateTimeField(default=timezone.now)
    # 文章更新时间,参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)
    # # PositiveIntegerField是用于存储正整数的字段
    # total_views = models.PositiveIntegerField(default=0)

    # 分类
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    # 标签
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='标签')

    def get_absolute_url(self):
        return reverse('detail', args=[self.id])

    class Meta:
        db_table = 'df_artice'
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.title

    pv=models.PositiveIntegerField(default=1)
    uv=models.PositiveIntegerField(default=1)

    @classmethod
    def host_posts(cls):
        return cls.objects.filter(status=1).order_by('-pv')

    @classmethod
    def latest_posts(cls):
        return cls.objects.filter(status=1).order_by('uv')