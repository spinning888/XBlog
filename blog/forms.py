from django import forms
from .models import Post, Profile, Comment

class PostForm(forms.ModelForm):
    # 非模型字段：用于输入或新建分类名
    category_name = forms.CharField(
        required=False,
        label="分类",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "分类（如：Python）"})
    )

    class Meta:
        model = Post
        fields = ["title", "content", "category_name"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "标题"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 10, "placeholder": "正文（支持Markdown）"}),
        }

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]
        widgets = {
            # 使用普通 FileInput，移除默认的“清除”复选框
            "avatar": forms.FileInput(attrs={"class": "form-control"})
        }


class ProfileInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio"]
        widgets = {
            "bio": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "写一句你的个人宣言（最多200字）"
            })
        }
        labels = {"bio": "个人宣言"}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "写下你的评论…"
            })
        }
