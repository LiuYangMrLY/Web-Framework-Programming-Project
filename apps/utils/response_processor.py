import json

from django.http import HttpResponse


def process_response(content: dict) -> HttpResponse:
    """
    将键值对字典 dict 转化为 JSON 格式, 并包装成 HttpResponse 对象.

    :param content: 要进行转化的字典 dict
    :return: 包装后的 HttpResponse 对象
    """
    content = json.dumps(content)

    return HttpResponse(content,
                        content_type='application/json;charset=utf-8',
                        status='200',
                        charset='utf-8')
