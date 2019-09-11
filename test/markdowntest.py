import markdown


def md2html(mdstr):
    # 扩展
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
            'markdown.extensions.toc']

    html1 = '''
    {% extends "blog/base.html" %}
{% load static %}


{% block css %}
<link href="{% static 'css/md_default.css' %}" rel="stylesheet">
{% endblock %}

{% block page_header %}
 <!-- Page Header -->
  <header class="masthead" style="background-image: url({{ content_img.url }})">
    <div class="overlay"></div>
    <div class="container">
      <div class="row">
        <div class="col-lg-8 col-md-10 mx-auto">
          <div class="post-heading">
            <h1>{{ title }}</h1>
            <h2 class="subheading">{{ subtitle }}</h2>
            <span class="meta">Posted by
              <a href="{{ href }}">{{ name }}</a>
              on {{ date }}</span>
          </div>
        </div>
      </div>
    </div>
  </header>

{% endblock %}

{% block main_content %}
  <!-- Post Content -->
  <article>
    <div class="container">
      <div class="row">
        <div class="col-lg-8 col-md-10 mx-auto" style='font-family: "Roboto","Helvetica","Arial",sans-serif'>
    '''
    html2 = """</div>
      </div>
    </div>
  </article>
{% endblock %}"""

    ret = markdown.markdown(mdstr, extensions=exts)
    return html1 + ret + html2


if __name__ == '__main__':

    with open("表结构.md", 'r', encoding="utf-8")as f:
        md = f.read()

    with open("md.html", 'w', encoding="utf-8")as f1:
        f1.write(md2html(md))

