import requests

from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views import View

from blog.models import Index, Navigation, Footer, Article, Comment
from djangoMyBlog.settings import AJAX_DATA

from user_agents import parse

from blog.AIComment import check_comment


def get_context_dict(request, is_article=None):
    nav_obj = Navigation.objects.filter(is_show=True)
    footer_obj = Footer.objects.filter(is_show=True)
    context_dict = {
        "navigation": nav_obj,
        "footer": footer_obj,
    }
    if not is_article:
        index_obj = Index.objects.get(url=request.path_info)
        context_dict.update({
            "title": index_obj.title,
            "header_title": index_obj.header_title,
            "header_subtitle": index_obj.header_subtitle,
            "header_img": index_obj.header_img,
        })
        return context_dict
    else:
        return context_dict


def index(request):
    """
    首页
    :param request:
    :return:
    """
    context_dict = get_context_dict(request)
    content_list = Article.objects.order_by("-mod_date").values()[:10]
    context_dict.update({"articles": content_list})
    return render(request, "blog/index.html", context=context_dict)


def about(request):
    """
    关于我
    :param request:
    :return:
    """
    context_dict = get_context_dict(request)
    return render(request, "blog/about.html", context_dict)


def article(request, year, month, day, filename):
    """
    文章
    """
    context_dict = get_context_dict(request, is_article=True)
    # time = datetime.strptime(f"{year}-{month}-{day}", '%Y-%m-%d')
    name = f"{year}{month}{day}{filename}.html"
    obj = Article.objects.get(url=request.path_info)
    context_dict.update({
        "title": obj.title,
        "subtitle": obj.subtitle,
        "date": obj.add_date,
        "name": obj.name,
        "href": obj.name_href,
        "content_img": obj.content_img,
    })
    return render(request, f"article/{name}", context_dict)


class OlderArticles(View):
    """
    往期文章
    """

    # context_dict = get_context_dict(request)
    # content_list = Article.objects.order_by("-mod_date").values()
    # context_dict.update({"articles": content_list})
    # return render(request, "blog/post.html", context_dict)
    def get(self, request):
        context_dict = get_context_dict(request)
        articles_list = Article.objects.order_by("-mod_date").values()

        paginator = Paginator(articles_list, 10)
        page = request.GET.get('page')
        try:
            articles = paginator.page(page)
        # 捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            articles = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return redirect('not_found')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            articles = paginator.page(paginator.num_pages)
        context_dict.update({"articles": articles})
        return render(request, "blog/post.html", context_dict)


class CommentList(View):
    def get(self, request):
        context_dict = get_context_dict(request)
        comment_list = Comment.objects.filter(is_show=True).order_by("-date", "-id").values()

        paginator = Paginator(comment_list, 10)
        page = request.GET.get('page')
        try:
            comment = paginator.page(page)
        # 捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            comment = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return redirect('not_found')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            comment = paginator.page(paginator.num_pages)
        total = Comment.objects.filter(is_show=True).count()
        context_dict.update({"comments": comment, "total": total})
        return render(request, "blog/comment.html", context_dict)

    def post(self, request):
        ip_address_dict = self.get_ip_address(request)
        data = request.POST
        if len(data["username"]) == 0 or len(data["content"]) == 0 or len(data["username"]) > 15 or len(
                data["content"]) > 200:
            return redirect('not_found')
        dic = {
            "username": data["username"],
            "content": data["content"],
            "ua": data["ua"],
        }
        if check_comment(data["content"]) == 0:
            dic.update({"is_show": True})
        ua_dict = self.analyze_ua(data["ua"])
        dic.update(ip_address_dict)
        dic.update(ua_dict)
        Comment.objects.create(**dic)
        AJAX_DATA["path"] = "/blog/comment.html"
        return JsonResponse(AJAX_DATA)

    @staticmethod
    def analyze_ua(ua):
        """
        分析ua,添加操作系统,浏览器
        """
        sys_opt = str(parse(ua)).split("/")
        ua_dict = {"system": sys_opt[1].strip(), "browser": sys_opt[2].strip()}
        return ua_dict

    @staticmethod
    def get_ip_address(request):
        """
        分析ip地址,添加ip,国家,城市
        """
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        err_dict = {"ip": ip, "country": "火星", "city": "未知"}

        url = "http://www.ip-api.com/json/" + ip
        try:
            response = requests.get(url).json()
        except Exception:
            return err_dict
        if response["status"] == "success":
            return {"ip": ip, "country": response["country"], "city": response["city"]}
        else:
            return err_dict


def page_not_found(request):
    return render(request, "404.html")


def page_error(request):
    return render(request, "500.html")
