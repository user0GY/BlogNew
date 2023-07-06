from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry
from django.contrib.admin import ModelAdmin
from apps.blog.models import Post,Category,Tag
from apps.blog.adminforms import PostAdminForms
from BlogNew.custom_site import custom_site
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','status','is_nav','create_time','post_count')
    fields=('name','status','is_nav')
    # inlines = ['PostInline',]
    def save_model(self, request, obj, form, change):
        obj.author=request.user
        return super(CategoryAdmin,self).save_model(request, obj, form, change)
    def post_count(self,obj):
        #大家使用 Django 创建模型的时候一定会经常使用 ForeignKey 来创建两个表格之间多对一的外键关系,例如B中有一个 models.ForeignKey(A) 。
        #而当我们需要反向查询 A 中某个具体实例所关联的 B 时，可能会用到 A.B_set.all() 或 B.objects.filter(A) 这两种不同的方法。
        #应该是有个叫post的model存在一个到ModelA的外键，自动为ModelA反向生成一个字段,方向外键
        return obj.post_set.count()
    post_count.short_description='文章数量'


class CategoryFilter(admin.SimpleListFilter):
    title = '分类过滤器'
    #应在该筛选器的查询字符串中使用的参数。
    parameter_name = 'author_category'


#modele表示当前过滤器所属的模块，可以有很多过滤器然后表示模块
    def lookups(self, request, module):
        #values
# values(*fields)
# 返回一个ValuesQuerySet —— QuerySet 的一个子类，迭代时返回字典而不是模型实例对象。
#
# 每个字典表示一个对象，键对应于模型对象的属性名称。
#
# 下面的例子将values() 与普通的模型对象进行比较：
        #返回一个类似列表
        return Category.objects.filter(author=request.user).values_list('id','name')

    def queryset(self, request, queryset):
        category_id=self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'create_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForms
    list_display = ['title', 'category', 'created_time', 'status','operator','author']
    #控制 list_display 中的字段是否以及哪些字段应链接到对象的“change” 页面。
    # 默认情况下，更改列表页面会将第一列 (list_display 中指定的第一个字段)链接到每个项目的更改页面。
    list_display_links = []
    list_filter = [CategoryFilter]
    #在管理更改列表页面上启用搜索框。这应该被设置为字段名的列表，每当有人在该文本框中提交搜索查询时，就会被搜索到。
    search_fields = ['title','category_name']
    #控制操作栏在页面上的显示位置
    actions_on_top = True
    # actions_on_bottom = True
    save_on_top = True

    # fields = (
    #     #选择标签和标题绑定
    #     ('category','title'),
    #     'content',
    #     'status',
    #     'body',
    #     'tag',
    # )
    fieldsets = (
        ('基础配置',{
            'description':'基础配置描述',
            'fields':(
                ('title','category'),
                'status',
            ),
        }),
        ('内容',{
            'fields':(
                'content',
                'body',
            ),
        }),
        ('额外内容', {
            'fields':('tag',),
        }),
    )
    # filter_horizontal = ('tag',)



    def operator(self,obj):
        return format_html(
            '<a herf="{}">编辑</a>',
            reverse('cus_admin:blog_post_change',args=(obj.id,))
        )
    operator.short_description='操作'

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def display_author(self,obj):
        return obj.author
    display_author.short_description = '作者'


    def get_queryset(self, request):
        #get_queryset
        # 正如其名，该方法可以返回一个量身定制的对象列表。
        # 当我们使用Django自带的ListView展示所有对象列表时，ListView默认会返回Model.objects.all()。
        return super(PostAdmin,self).get_queryset(request).filter(author=request.user)

    exclude = ('author',)

    #内部类 样式
    # class Media:
    #     css={
    #         'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
    #     }
    #     js=("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/botstrap.bundule.js",)

#
# class PostInline(admin.TabularInline):
#     fields = ('title','content')
#     extra = 1
#     model = Post


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr','object_id','action_flag','user','change_message',]

custom_site.register(Post)
custom_site.register(Tag)
custom_site.register(Category)



