import random
import uuid
import string
from random import randint as rdint
from io import BytesIO as StringIO

from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse

from web import settings


class Captcha:
    def __init__(self, width=200, height=50, fontSize=35, num=4, bgColor='#ffffff'):
        self.width = width  # 生成图片宽度
        self.height = height  # 生成图片高度
        self.num = num  # 验证码字符个数
        self.bgColor = bgColor  # 生成图片背景颜色
        self.fontPath = '{}/arialbd.ttf'.format(settings.BASE_DIR).replace('\\', '/')  # # 字体大小
        self.font = ImageFont.truetype(self.fontPath, fontSize)  # 字体大小
        self.code = ''
        self.codename = str(uuid.uuid1())  # 验证码文件名
        self.img = Image.new('RGB', (self.width, self.height), self.bgColor)  # 生成图片对象

    # 获取随机颜色，RGB格式
    def get_random_Color(self):
        c1 = rdint(50, 150)
        c2 = rdint(50, 150)
        c3 = rdint(50, 150)
        return c1, c2, c3

    # 随机生成1位字符,作为验证码内容
    def get_random_char(self):
        c = ''.join(random.sample(string.ascii_letters, 1))
        self.code += c
        return c

    # 生成随机位置(x,y)
    def get_random_xy(self):
        x = rdint(0, int(self.width))
        y = rdint(0, int(self.height))
        return x, y

    # 图片旋转
    def rotate(self):
        deg = int(self.height / 3)  # 旋转角度
        self.img = self.img.rotate(rdint(0, deg), expand=0)

    # 画n条干扰线
    def drawLine(self, n):
        draw = ImageDraw.Draw(self.img)
        for i in range(n): draw.line([self.get_random_xy(), self.get_random_xy()], self.get_random_Color())
        del draw

    # 画n个干扰点
    def drawPoint(self, n):
        draw = ImageDraw.Draw(self.img)
        for i in range(n):
            draw.point([self.get_random_xy()], self.get_random_Color())
        del draw

    def getsize(font, text):
        if hasattr(font, 'getoffset'):
            return tuple([x + y for x, y in zip(font.getsize(text), font.getoffset(text))])
        else:
            return font.getsize(text)

    # 写验证码内容
    def drawText(self, position, char, fillColor):
        draw = ImageDraw.Draw(self.img)
        draw.text(position, char, font=self.font, fill=fillColor)
        # params = (1 - float(random.randint(1, 2)) / 100,
        #           0,
        #           0,
        #           0,
        #           1 - float(random.randint(1, 10)) / 100,
        #           float(random.randint(1, 2)) / 500,
        #           0.001,
        #           float(random.randint(1, 2)) / 500,
        #           )
        # self.img = self.img.transform(self.img.size, Image.PERSPECTIVE, params)
        del draw

    # 生成验证码图片，并返回图片对象
    def getVertifyImg(self):
        x_start = 2
        y_start = 0
        for i in range(self.num):
            x = x_start + i * int(self.width / (self.num))
            y = rdint(y_start, int(self.height / 3))
            self.drawText((x, y), self.get_random_char(), self.get_random_Color())
        self.drawLine(3)
        self.drawPoint(60)
        return self.img

    def saveInMemory(self, request):
        img = self.getVertifyImg()
        request.session['captcha'] = self.code
        f = StringIO()  # 开辟内存空间
        img.save(f, 'png')
        return f.getvalue()

    def saveInDict(self):
        img = self.getVertifyImg()
        path = '{}.png'.format(self.codename)
        img.save(path, 'png')
        return self.code, 'media/captcha/{}.png'.format(self.codename)


def get_captcha_img(request):
    img = Captcha()

    return HttpResponse(img.saveInMemory(request),
                        content_type='image/png',
                        status='200',
                        reason='ok',
                        charset='utf-8')
