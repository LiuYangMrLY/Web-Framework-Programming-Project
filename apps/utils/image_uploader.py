import re

import magic
from PIL import ImageFile
from django_redis import get_redis_connection

from web import settings
from apps.utils.response_processor import process_response
from apps.utils.random_string_generator import Pattern, generate_string
from apps.account import models as account_models


def upload(request):
    if not request.method == 'POST':
        return process_response({'code': '002', 'msg': '请求方法错误'})
    else:
        # 图片 image 验证
        img = request.FILES.get('img')
        if not img:
            return process_response({'code': '004', 'msg': '缺少图片'})

        # 文件大小
        if img.size > settings.IMAGE_MAX_SIZE:
            return process_response({'code': '005', 'msg': '图片过大'})

        # 文件后缀名初步判断文件类型
        extension = img.name.split('.')[-1]
        if extension not in settings.ALLOWED_IMAGE_EXTENSION:
            return process_response({'code': '006', 'msg': '图片文件仅支持 jpg, png 格式'})

        # 附加时间的随机图片名
        name = generate_string(10, Pattern.Letters_And_Digits, True)

        # 图片保存路径
        path = settings.IMAGE_PATH + name + '.' + extension

        # 储存图片
        parser = ImageFile.Parser()
        for chunk in img.chunks():
            parser.feed(chunk)
        f = parser.close()
        f.save(path)

        if not re.search(settings.ALLOWED_IMAGE_EXTENSION[extension], magic.from_file(path)):
            return process_response({'code': '006', 'msg': '图片文件仅支持 jpg, png 格式'})

        info = account_models.User.objects.filter(username='Leo').first().info
        info.avatar = path
        info.save()

        conn = get_redis_connection('default')
        conn.set('save', '')

        return process_response({'path': path, 'code': '000', 'msg': '上传成功'})
