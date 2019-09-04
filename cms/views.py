import json
import os
from datetime import datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from cms.img_code import make_valid_img

from blog.forms import IndexForm, NavigationForm, FooterForm, ArticleForm, CommentForm, AboutForm
from cms.md2about import md2about
from cms.md2html import md2html
from djangoMyBlog.settings import IMG_PATH, AJAX_DATA, MEDIA_ROOT, TEMPLATES
from blog.models import Index, Navigation, Footer, Article, Comment, About
from django.forms.models import modelformset_factory


class Login(View):
    def get(self, request):
        return render(request, 'cms/login.html')

    def post(self, request):
        request.session.clear_expired()  # 清空过期的session
        dic = json.loads(request.body.decode('utf-8'))
        # print(dic)
        if dic['code'].upper() == request.session['valid_str'].upper():
            user_obj = auth.authenticate(username=dic['username'], password=dic['password'])
            if user_obj:
                auth.login(request, user_obj)
                if not dic['remember']:
                    request.session.set_expiry(0)

                if request.GET.get('next'):
                    path = request.GET.get('next')
                else:
                    path = '/cms'
                return JsonResponse({'status': 1, 'path': path})
            else:
                return JsonResponse({'status': 0, 'error': '用户名密码错误'})
        else:
            return JsonResponse({'status': 0, 'error': '验证码错误'})


def get_valid_img(request):
    sum_str, data = make_valid_img()
    request.session['valid_str'] = sum_str
    return HttpResponse(data)


@login_required
def cms_home(request):
    return render(request, "cms/cms_base.html")


@method_decorator(login_required, name='dispatch')
class PageIndex(View):
    def get(self, request):
        index_obj = Index.objects.all()
        index_thead = [i for i in IndexForm.Meta.labels.values()]
        dic = {
            "index_obj": index_obj,
            "index_thead": index_thead,
        }
        dic.update({"title": "封面管理"})
        return render(request, "cms/page_index.html", dic)

    def post(self, request):
        """
        post请求删除index
        """
        pk = request.POST.get("id")
        Index.objects.filter(id=pk).delete()

        return JsonResponse(AJAX_DATA)


@method_decorator(login_required, name='dispatch')
class PageEdit(View):
    """
    添加/编辑index,nav,footer
    """

    def get(self, request):
        opt = request.GET.get("opt")
        if not opt:
            # 添加form
            form_dict = self.get_form_dict()
        else:
            # 编辑form
            form_dict = self.get_form_obj(opt, request)
        return render(request, "cms/page_edit.html", form_dict)

    def post(self, request):
        opt = request.POST.get("opt")
        # print(opt)
        if hasattr(self, opt):
            func = getattr(self, opt)
            if callable(func):
                pk = request.GET.get("id")
                return JsonResponse(func(request, pk))
            else:
                return
            # TODO 404
        else:
            return

    def index(self, request, pk):
        if pk:
            index_obj = Index.objects.get(id=pk)
            form_obj = IndexForm(request.POST, request.FILES, instance=index_obj)
        else:
            form_obj = IndexForm(request.POST, request.FILES)
        if form_obj.is_valid():
            form_obj.save()
            file_obj = request.FILES.get('header_img')
            if file_obj:
                file_name = file_obj.name
                file_path = os.path.join(IMG_PATH, file_name)
                with open(file_path, 'wb')as f:
                    for data in file_obj:
                        f.write(data)
            AJAX_DATA["path"] = "/cms/page/index"
            return AJAX_DATA
        else:
            AJAX_DATA["status"] = form_obj.errors
            return AJAX_DATA

    def nav(self, request, pk):
        if pk:
            nav_obj = Navigation.objects.get(id=pk)
            form_obj = NavigationForm(request.POST, instance=nav_obj)
        else:
            form_obj = NavigationForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            AJAX_DATA["path"] = "/cms/page/nav_footer"
            return AJAX_DATA
        else:
            AJAX_DATA["status"] = form_obj.errors
            return AJAX_DATA

    def footer(self, request, pk):
        if pk:
            footer_obj = Footer.objects.get(id=pk)
            form_obj = FooterForm(request.POST, instance=footer_obj)
        else:
            form_obj = FooterForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            AJAX_DATA["path"] = "/cms/page/nav_footer"
            return AJAX_DATA
        else:
            print(form_obj.errors)
            AJAX_DATA["status"] = form_obj.errors
            return AJAX_DATA

    def get_form_obj(self, opt, request):
        """
        获取form对象,调用get_form_dict返回form_dict
        :param opt: index/nav/footer
        :param request:
        :return:
        """
        pk = request.GET.get("id")
        opt_model = {"index": self.get_form_dict(index=Index.objects.filter(id=pk).first()),
                     "nav": self.get_form_dict(nav=Navigation.objects.filter(id=pk).first()),
                     "footer": self.get_form_dict(footer=Footer.objects.filter(id=pk).first())}

        return opt_model[opt]

    def get_form_dict(self, index=None, nav=None, footer=None):
        index_form = IndexForm(instance=index)
        nav_form = NavigationForm(instance=nav)
        footer_form = FooterForm(instance=footer)
        form_dict = {
            "index_form": index_form,
            "nav_form": nav_form,
            "footer_form": footer_form,
        }
        return form_dict


@method_decorator(login_required, name='dispatch')
class PageNavFooter(View):
    def get(self, request):
        nav_obj = Navigation.objects.all()
        footer_obj = Footer.objects.all()
        nav_thead = [i for i in NavigationForm.Meta.labels.values()]
        footer_thead = [i for i in FooterForm.Meta.labels.values()]
        dic = {
            "nav_obj": nav_obj,
            "footer_obj": footer_obj,
            "nav_thead": nav_thead,
            "footer_thead": footer_thead,
        }
        dic.update({"title": "导航/社交管理"})
        return render(request, "cms/page_nav_footer.html", dic)

    def post(self, request):
        """
        post请求删除nav/footer
        """
        pk = request.POST.get("id")
        opt_dict = {"nav": Navigation, "footer": Footer}
        opt_dict[request.POST.get("opt")].objects.filter(id=pk).delete()
        return JsonResponse(AJAX_DATA)


@method_decorator(login_required, name='dispatch')
class ArticleList(View):
    def get(self, request):
        content_obj = Article.objects.all()
        content_thead = [i for i in ArticleForm.Meta.labels.values()]
        dic = {
            "content_obj": content_obj,
            "content_thead": content_thead,
        }
        dic.update({"title": "文章管理"})
        return render(request, "cms/article_show.html", dic)

    def post(self, request):
        pk = request.POST.get("id")
        Article.objects.filter(id=pk).delete()
        return JsonResponse(AJAX_DATA)


@method_decorator(login_required, name='dispatch')
class ArticleEdit(View):
    def get(self, request):
        pk = request.GET.get("id")
        article_obj = Article.objects.get(id=pk) if pk else None
        form_obj = ArticleForm(instance=article_obj)
        form_dict = {"article_form": form_obj}
        return render(request, "cms/article_edit.html", form_dict)

    def post(self, request):
        pk = request.GET.get("id")
        article_obj = Article.objects.get(id=pk) if pk else None
        dic = request.POST.dict()
        date = dic.pop("add_date")
        dic.update({"add_date": datetime.strptime(date, '%Y-%m-%d')})
        form_obj = ArticleForm(dic, request.FILES, instance=article_obj)
        if form_obj.is_valid():
            form_obj.save()
            self.make_md()
            AJAX_DATA["path"] = "/cms/article"
            return JsonResponse(AJAX_DATA)
        else:
            AJAX_DATA["status"] = form_obj.errors
            return JsonResponse(AJAX_DATA)

    @staticmethod
    def make_md():
        # 取出修改日期最后的文章
        article_obj = Article.objects.order_by("mod_date").last()

        # 读markdown
        file = article_obj.file.name
        md_file_path = os.path.join(MEDIA_ROOT, file)
        with open(md_file_path, 'r', encoding="utf-8")as f:
            md = f.read()

        # 将markdown写入html
        filename = datetime.strftime(article_obj.add_date, '%Y%m%d') + f"{file[8:].split('.md')[0]}"
        html_path = os.path.join(TEMPLATES[0]["DIRS"][0], "article", filename + ".html")
        with open(html_path, 'a', encoding="utf-8")as f:
            f.write(md2html(md))

        # 修改该文章的url
        url = f"/blog/{filename[0:4]}/{filename[4:6]}/{filename[6:8]}/{filename[8:]}.html"
        Article.objects.filter(id=article_obj.id).update(url=url)


@method_decorator(login_required, name='dispatch')
class CommentList(View):
    def get(self, request):
        comment_obj = Comment.objects.all()
        comment_thead = [i for i in CommentForm.Meta.labels.values()]
        dic = {
            "comment_obj": comment_obj,
            "comment_thead": comment_thead,
        }
        dic.update({"title": "留言管理"})
        return render(request, "cms/comment_list.html", dic)

    def post(self, request):
        opt = request.POST.get("opt")
        if hasattr(self, opt):
            func = getattr(self, opt)
            if callable(func):
                return JsonResponse(func(request))

    @staticmethod
    def change(request):
        id_list = request.POST.getlist("id_list[]")
        Comment.objects.filter(id__in=id_list).update(is_show=True)
        return AJAX_DATA

    @staticmethod
    def refuse(request):
        id_list = request.POST.getlist("id_list[]")
        Comment.objects.filter(id__in=id_list).update(is_show=False)
        return AJAX_DATA

    @staticmethod
    def delete(request):
        pk = request.POST.get("id")
        Comment.objects.filter(id=pk).delete()
        return AJAX_DATA


@method_decorator(login_required, name='dispatch')
class CommentEdit(View):
    def get(self, request):
        pk = request.GET.get("id")
        comment_obj = Comment.objects.get(id=pk) if pk else None
        form_obj = CommentForm(instance=comment_obj)
        form_dict = {"comment_form": form_obj}
        return render(request, "cms/comment_edit.html", form_dict)

    def post(self, request):
        pk = request.GET.get("id")
        comment_obj = Comment.objects.get(id=pk) if pk else None
        dic = request.POST.dict()
        date = dic.pop("date")
        dic.update({"date": datetime.strptime(date, '%Y-%m-%d')})
        form_obj = CommentForm(dic, instance=comment_obj)
        if form_obj.is_valid():
            form_obj.save()
            AJAX_DATA["path"] = '/cms/comment'
            return JsonResponse(AJAX_DATA)
        else:
            AJAX_DATA["status"] = form_obj.errors
            return JsonResponse(AJAX_DATA)


@method_decorator(login_required, name='dispatch')
class AboutHtml(View):
    def get(self, request):
        form_obj = AboutForm()
        form_dict = {"about_form": form_obj}
        return render(request, "cms/about_edit.html", form_dict)

    def post(self, request):
        form_obj = AboutForm(files=request.FILES)
        if form_obj.is_valid():
            form_obj.save()

            about_obj = About.objects.first()

            # 读markdown
            file = about_obj.file.name
            md_file_path = os.path.join(MEDIA_ROOT, file)
            with open(md_file_path, 'r', encoding="utf-8")as f:
                md = f.read()

            # 将markdown写入html
            about_html = os.path.join(TEMPLATES[0]["DIRS"][0], "blog", "about.html")
            with open(about_html, 'w', encoding="utf-8")as f:
                f.write(md2about(md))

            # 删除
            os.remove(md_file_path)
            About.objects.first().delete()

            AJAX_DATA['path'] = '/blog/about.html'
            return JsonResponse(AJAX_DATA)

        AJAX_DATA["status"] = form_obj.errors
        return JsonResponse(AJAX_DATA)
