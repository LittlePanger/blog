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
from django.conf.urls.static import static
from django.contrib import admin

from blog.views import page_not_found,page_error
from djangoMyBlog import settings
from django.conf.urls import handler404, handler500

# from django.views import static
# from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', index),
    url(r"^", include("blog.urls")),
    url(r"^blog/", include("blog.urls")),
    url(r"^cms/", include("cms.urls")),
    url(r'^404/', page_not_found, name='not_found'),
    url(r'^500/', page_error, name='error'),
    # url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='media'),
    # url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}, name='media')
]
# handler404 = 'blog.views.page_not_found'
# handler500 = 'blog.views.page_error'
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
