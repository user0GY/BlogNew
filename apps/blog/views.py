from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render,HttpResponse

from .form import SearchForm
from .models import Post,Tag,Category
from django.views.generic import View
from apps.config.models import SideBar
from django.views.generic import ListView
from apps.comment.models import Comment
# Create your views here.
def post_list(request,category_id=None,tag_id=None):
    #context 属于提前赋值了
    category=None
    tag=None
    categorys = Category.objects.all()
    tags=Tag.objects.all()
    if tag_id:
        #如果查询的是标签列表
        try:
            #展示列表
            tag=Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            #没有该标签
            post_list=[]
        else:
            #展示现有的标签
            post_list=tag.post_set.filter(status=1)
    else:
        # 如果查询的是分类列表
        post_list = Post.objects.filter(status=1)
        if category_id:
            #这里的category_id是外键，django的命名是外键_id
            try:
                category=Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                category=None
            else:
                post_list=post_list.filter(category_id=category_id)
    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context={
        'category':category,
        'tag':tag,
        'post_list':post_list,
        'categorys':categorys,
        'sidebars':SideBar.get_all(),
        'tags':tags,
        'articles':articles,
    }
    return render(request,'blog/list.html',context=context)


def post_detail(request,post_id):
    try:
        post=Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post= None
    comment=Comment.objects.filter(article_id=post_id)
    return render(request,'blog/detail.html',context={'post':post,'comment':comment})

# class Search(View):
#     def post(self,request):
#         search_context=SearchForm(data=request.POST)
#         if search_context.is_valid():
#             # 保存数据，但暂时不提交到数据库中
#             new_article = search_context.save(commit=False)
#             # 作者为当前请求的用户名
#         try:
#             search_result=Post.objects.get(title=search_context)
#         except Post.DoesNotExist:
#             search_result=None
#
#     def get(self,request):
#         search_context=SearchForm()
#         context={
#
#         }
#         return render(request,'blog/detainl.html',context)

class IndexView(ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'

class SearchView(IndexView):
    def get_context_data(self):
        context =super().get_context_data()
        context.update(
            {
                'keyword':self.request.GET.get('keyword','')
            }
        )
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title_icontains=keyword) | Q(desc_icontains=keyword))





