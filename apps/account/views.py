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

        # 数据经过中间件处理存放在 request.json_data 中
        json_data = request.json_data

        # 验证码 captcha 检验
        captcha = json_data['captcha']
        if request.session.get('captcha', '').lower() != captcha.lower():
            content['code'] = '004'
            content['msg'] = '验证码错误'
            return process_response(content)

        # 用户名 username 检验
        username = json_data['username']
        result = validate_username(username)
        if result:
            content['code'] = result[0]
            content['msg'] = result[1]
            return process_response(content)

        # 密码 password 验证
        password = json_data['password']
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
