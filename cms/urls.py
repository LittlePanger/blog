"""djangoMyBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from cms.views import Login, get_valid_img, cms_home, \
    PageIndex, PageEdit, PageNavFooter, ArticleList, ArticleEdit, CommentList, CommentEdit,AboutHtml

urlpatterns = [
    # 认证
    url(r'^login', Login.as_view(), name='login'),
    url(r'^get_valid_img', get_valid_img, name='get_valid_img'),
    url(r'^$', cms_home, name='cms_home'),

    # 页面管理
    url(r'^page/index', PageIndex.as_view(), name='page_index'),
    url(r'^page/edit', PageEdit.as_view(), name='page_edit'),
    url(r'^page/nav_footer', PageNavFooter.as_view(), name='page_nav_footer'),

    # 文章管理
    url(r'^article$', ArticleList.as_view(), name='article'),
    url(r'^article/edit', ArticleEdit.as_view(), name='article_edit'),

    # 留言管理
    url(r'^comment$', CommentList.as_view(), name='comment'),
    url(r'^comment/edit', CommentEdit.as_view(), name='comment_edit'),

    # 关于
    url(r'abouthtml',AboutHtml.as_view(),name='about_html')
]
