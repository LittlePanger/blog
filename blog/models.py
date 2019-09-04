from django.db import models
from django.utils import timezone


class Index(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    header_title = models.CharField(max_length=100)
    header_subtitle = models.CharField(max_length=100, null=True)
    header_img = models.ImageField(upload_to='img')
    is_show = models.BooleanField(default=True)


class Navigation(models.Model):
    id = models.AutoField(primary_key=True)
    href = models.CharField(max_length=100)
    title = models.CharField(max_length=15)
    is_show = models.BooleanField(default=True)


class Footer(models.Model):
    id = models.AutoField(primary_key=True)
    href = models.CharField(max_length=100)
    fa = models.CharField(max_length=20)
    is_show = models.BooleanField(default=True)


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='md/file')
    url = models.CharField(max_length=100)
    add_date = models.DateTimeField(default=timezone.now)
    mod_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=32, default="LittlePanger")
    name_href = models.CharField(max_length=100, default="/")
    content_img = models.ImageField(upload_to='md/img')
    is_show = models.BooleanField(default=True)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=15)
    content = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)
    ua = models.CharField(max_length=200)
    system = models.CharField(max_length=30, default="Windows10")
    browser = models.CharField(max_length=30, default="Chrome")
    ip = models.GenericIPAddressField(default="127.0.0.1")
    country = models.CharField(max_length=20, default="China")
    city = models.CharField(max_length=20, default="Beijing")
    is_show = models.BooleanField(default=False)


class About(models.Model):
    file = models.FileField(upload_to='md/about')
