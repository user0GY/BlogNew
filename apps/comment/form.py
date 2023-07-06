from django import forms
from .models import Comment
class CommentForm(forms.ModelForm):
    # nickname = forms.CharField(
    #     label='昵称',
    #     max_length=50,
    #     widget=forms.widgets.Input(
    #         attrs={
    #             'class': 'form-control'
    #         }
    #     )
    # )
    #
    # email = forms.CharField(
    #     label='Email',
    #     max_length=50,
    #     widget=forms.widgets.EmailInput(
    #         attrs={
    #             'class': 'form-control'
    #         }
    #     )
    # )
    body = forms.CharField(
        label='内容',
        max_length=500,
        widget=forms.widgets.Textarea(
                attrs={
                'rows': 6,
                'cols':60,
                'class':'form-control'
            }
        )
    )
    #
    # def clean_content(self):
    #     content=self.cleaned_data.get('content')
    #     return content
    class Meta:
        model = Comment
        fields = ['nick_name','email','body']