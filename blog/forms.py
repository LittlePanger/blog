from django import forms
from django.core.exceptions import ValidationError

from blog.models import Index, Navigation, Footer, Article, Comment, About


class IndexForm(forms.ModelForm):
    class Meta:
        model = Index
        fields = "__all__"
        labels = {
            "url": "当前url",
            "title": "<title>",
            "header_title": "标题",
            "header_subtitle": "副标题",
            "header_img": "图片",
            "is_show": "展示"
        }
        widgets = {
            "is_show": forms.widgets.CheckboxInput(attrs={"id": "index_is_show"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != "header_img" and field != "is_show":
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'id': f'index_{field}'
                })

    def clean_url(self):
        value = self.cleaned_data.get("url")
        if value[0] != "/":
            raise ValidationError("必须以'/'开头")
        else:
            return value


class NavigationForm(forms.ModelForm):
    class Meta:
        model = Navigation
        fields = '__all__'
        labels = {
            "href": "链接",
            "title": "标题",
            "is_show": "展示"
        }
        widgets = {
            "is_show": forms.widgets.CheckboxInput(attrs={"id": "nav_is_show"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != "is_show":
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'id': f'nav_{field}'
                })

    def clean_href(self):
        value = self.cleaned_data.get("href")
        if value[0] != "/":
            raise ValidationError("必须以'/'开头")
        else:
            return value


class FooterForm(forms.ModelForm):
    class Meta:
        model = Footer
        fields = '__all__'
        labels = {
            "href": "链接",
            "fa": "图标",
            "is_show": "展示"
        }
        help_texts = {
            "fa": "fa-github"
        }
        widgets = {
            "is_show": forms.widgets.CheckboxInput(attrs={"id": "footer_is_show"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != "is_show":
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'id': f'footer_{field}'
                })


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        labels = {
            "title": "标题",
            "subtitle": "副标题",
            "file": "markdown",
            "url": "链接",
            "add_date": "上传日期",
            "mod_date": "最后更新日期",
            "name": "作者",
            "name_href": "作者链接",
            "content_img": "文章封面",
            "is_show": "展示"
        }
        widgets = {
            "is_show": forms.widgets.CheckboxInput(attrs={"id": "article_is_show"}),
            "add_date": forms.widgets.DateInput(attrs={"id": "article_add_date", "type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != "content_img" and field != "is_show" and field != "file":
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'id': f'article_{field}'
                })


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        labels = {
            "username": "用户名",
            "content": "内容",
            "date": "日期",
            "ua": "User-Agent",
            "system": "系统",
            "browser": "浏览器",
            "ip": "IP",
            "country": "国家",
            "city": "城市",
            "is_show": "展示"
        }
        widgets = {
            "date": forms.widgets.DateTimeInput(attrs={"type": "date"}),
            "is_show": forms.widgets.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != "is_show":
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                })


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = "__all__"
        labels = {
            "file": "md"
        }


class CommentInputForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['username', 'content']
        labels = {
            "username": "昵称",
            "content": "留言",
        }
        widgets = {
            "username": forms.widgets.TextInput(attrs={"placeholder": "昵称", "id": "name"}),
            "content": forms.widgets.Textarea(attrs={"placeholder": "留言", "id": "message"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
