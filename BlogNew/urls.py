"""
URL configuration for BlogNew project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from BlogNew.custom_site import custom_site
from apps.blog.views import post_list,post_detail,SearchView
from apps.config.views import LinkListView
from apps.comment.views import post_comment
from apps import comment
from apps.userfile.views import user_register
urlpatterns = [
    re_path(r'^super_admin/', admin.site.urls,name='super_admin'),
    re_path(r'^admin/', custom_site.urls,name='admin'),
    re_path(r'^$',post_list,name='index'),
    re_path(r'category/(?P<category_id>\d+)/$',post_list,name='category-list'),
    re_path(r'tag/(?P<tag_id>\d+)/$',post_list,name='tag-list'),
    re_path(r'post/(?P<post_id>\d+).html$',post_detail,name='post-detail'),
    re_path(r'^links/$', LinkListView.as_view(),name='links'),
    re_path(r'^search/$',SearchView.as_view(),name='search'),
    re_path(r'^comment/(?P<id>\d+)/$', post_comment, name='comment'),
    re_path(r'^register/$', user_register, name='register'),

]
