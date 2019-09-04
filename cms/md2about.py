from imp import reload

import markdown
import sys

reload(sys)


def md2about(mdstr):
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
            'markdown.extensions.toc']

    html1 = '''
{% extends 'blog/base.html' %}


{% block page_header %}
    <!-- Page Header -->
    <header class="masthead" style="background-image: url({{ header_img.url }})">
        <div class="overlay"></div>
        <div class="container">
            <div class="row">
                <div class="col-lg-8 col-md-10 mx-auto">
                    <div class="page-heading">
                        <h1>{{ header_title }}</h1>
                        <span class="subheading">{{ header_subtitle }}</span>
                    </div>
                </div>
            </div>
        </div>
    </header>
{% endblock %}



{% block main_content %}
<!-- Main Content -->
<div class="container">
    <div class="row">
        <div class="col-lg-8 col-md-10 mx-auto" style='font-family: "Roboto","Helvetica","Arial",sans-serif'>
    '''
    html2 = """        </div>
    </div>
</div>

{% endblock %}"""

    ret = markdown.markdown(mdstr, extensions=exts)
    return html1 + ret + html2

