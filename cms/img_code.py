import os
import random

from PIL import Image, ImageDraw, ImageFont

from djangoMyBlog import settings
from django.http import HttpResponse


def make_valid_img():
    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    img_obj = Image.new('RGB', (150, 34), get_random_color())  # 图片对象
    draw_obj = ImageDraw.Draw(img_obj)  # 通过图片对象生成一个画笔对象
    font_path = os.path.join(settings.BASE_DIR, 'statics/font/Marlbow.ttf')  # 获取字体,注意有些字体文件不能识别数字，所以如果数字显示不出来，就换个字体
    font_obj = ImageFont.truetype(font_path, 30)  # 创建字体对象
    sum_str = ''  # 这个数据就是用户需要输入的验证码的内容
    for i in range(4):
        a = random.choice(
            [str(random.randint(0, 9)), chr(random.randint(97, 122)), chr(random.randint(65, 90))])  # 4  a  5  D  6  S
        sum_str += a
    print(sum_str)
    draw_obj.text((45, 0), sum_str, fill=get_random_color(), font=font_obj)  # 通过画笔对象，添加文字

    width = 150
    height = 34
    # 添加噪线
    for i in range(5):  # 添加了5条线
        # 一个坐标表示一个点，两个点就可以连成一条线
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw_obj.line((x1, y1, x2, y2), fill=get_random_color())
    # # 添加噪点
    for i in range(10):
        # 这是添加点，50个点
        draw_obj.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        # 下面是添加很小的弧线，看上去类似于一个点，50个小弧线
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw_obj.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())  # x, y是弧线的起始点位置，x + 4, y + 4是弧线的结束点位置

    from io import BytesIO
    f = BytesIO()  # 操作内存的把手
    img_obj.save(f, 'png')  #
    data = f.getvalue()
    return sum_str,data
