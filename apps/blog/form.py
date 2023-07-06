from django import forms
# 引入文章模型
from .models import Post

class SearchForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = Post
        # 定义表单包含的字段
        fields = ('title',)