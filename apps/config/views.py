from django.shortcuts import render,HttpResponse
from django.views.generic import ListView

from apps.blog.views import SideBar,Category
from .models import Link
# Create your views here.


class CommonViewMixin:
    #**kwargs就是传递一个可变参数列表给函数实参，这个参数列表的数目未知，甚至长度可以为0。
    def get_context_data(self,**kwargs):
        #context super（）保存
        context=super().get_context_data(**kwargs)
        context.update(
            {
                'sidebars':SideBar.get_all()
            }
        )
        # context.update(Category.get_navs())
        return context

class LinkListView(CommonViewMixin,ListView):
    queryset = Link.objects.filter(status=1)
    template_name = 'config/links.html'
    context_object_name = 'link_list'



