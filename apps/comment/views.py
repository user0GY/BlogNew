from django.shortcuts import render, get_object_or_404, redirect
from apps.blog.models import Post
from django.http import HttpResponse
from .form import CommentForm
from .models import Comment
from apps.config.views import CommonViewMixin


# Create your views here.

# def post_comment(request, post_id):
#     article = Post.objects.get(id=post_id)
#     # 处理 POST 请求
#     if request.method == 'POST':
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.user = request.user
#             new_comment.save()
#             return render(request,'blog/detail.html',context={'article':article})
#         else:
#             return HttpResponse("表单内容有误，请重新填写。")
#     # 处理错误请求
#     else:
#         article_post_form = CommentForm()
#         # 赋值上下文
#         context = {'article':article,'article_post_form': article_post_form}
#         return render(request, 'blog/detail.html', context)

def post_comment(request, id):
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        comment_post = request.POST
        # 保存数据，但暂时不提交到数据库中
        comment=Comment()
        comment.nick_name = request.POST['nickname']
        comment.email = request.POST['email']
        comment.body = request.POST['body']
        comment.status=1
        comment.article_id = id
        comment.save()
        # 完成后返回到文章列表
        return render(request,'blog/detail.html')
    # 如果数据不合法，返回错误信

    return render(request, 'config/comment.html')
