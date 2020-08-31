import json

from django.contrib.auth.hashers import make_password, check_password

from apps.account import models as account_models
from apps.utils.response_processor import process_response
from apps.utils.validator import validate_username, validate_password


def register(request):
    if not request.method == 'POST':
        return process_response({'code': '002', 'msg': '请求方法错误'})
    else:
        content = {}

        # JSON 格式检验
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            json_data = {}
        if not json_data:
            content['code'] = '001'
            content['msg'] = 'JSON 格式解析错误'
            return process_response(content)

        # 验证码 captcha 检验
        try:
            captcha = json_data['captcha']
        except KeyError:
            captcha = ''
        if not captcha:
            content['code'] = '003'
            content['msg'] = '缺少验证码'
            return process_response(content)
        if request.session.get('captcha', '') != captcha.lower():
            content['code'] = '004'
            content['msg'] = '验证码错误'
            return process_response(content)

        # 用户名 username 检验
        try:
            username = json_data['username']
        except KeyError:
            username = ''
        if not username:
            content['code'] = '101'
            content['msg'] = '缺少用户名'
            return process_response(content)
        result = validate_username(username)
        if result:
            content['code'] = result[0]
            content['msg'] = result[1]
            return process_response(content)

        # 密码 password 验证
        try:
            password = json_data['password']
        except KeyError:
            password = ''
        if not password:
            content['code'] = '111'
            content['msg'] = '缺少密码'
            return process_response(content)
        result = validate_password(password)
        if result:
            content['code'] = result[0]
            content['msg'] = result[1]
            return process_response(content)

        # 用户名 username 存在性验证
        if account_models.User.objects.filter(username=username):
            content['code'] = '121'
            content['msg'] = '用户名已存在'
            return process_response(content)

        # 创建用户 user 和 用户信息 user_info
        user = account_models.User(username=username,
                                   password=make_password(password)
                                   )
        user.save()
        user_info = account_models.UserInfo(user=user)
        user_info.save()

        content['code'] = '000'
        content['msg'] = '注册成功'

        return process_response(content)


