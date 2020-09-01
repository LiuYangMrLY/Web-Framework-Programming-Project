import json

from django.contrib.auth.hashers import make_password, check_password

from apps.account import models as account_models
from apps.utils.response_processor import process_response
from apps.utils.validator import validate_username, validate_password


def register(request):
    if not request.method == 'POST':
        return process_response({'code': '002', 'msg': '请求方法错误'})
    else:
        # 数据经过中间件处理存放在 request.json_data 中
        json_data = request.json_data

        # 验证码 captcha 检验
        captcha = json_data['captcha']
        if request.session.get('captcha', '').lower() != captcha.lower():
            return process_response({'code': '004', 'msg': '验证码错误'})
        del request.session['captcha']

        # 用户名 username 格式检验
        username = json_data['username']
        result = validate_username(username)
        if result:
            return process_response({'code': result[0], 'msg': result[1]})

        # 密码 password 格式验证
        password = json_data['password']
        result = validate_password(password)
        if result:
            return process_response({'code': result[0], 'msg': result[1]})

        # 用户名 username 存在性验证
        if account_models.User.objects.filter(username=username):
            return process_response({'code': '121', 'msg': '用户名已存在'})

        # 创建用户 user 和 用户信息 user_info
        user = account_models.User(username=username,
                                   password=make_password(password)
                                   )
        user.save()
        user_info = account_models.UserInfo(user=user)
        user_info.save()

        return process_response({'code': '000', 'msg': '注册成功'})


def login(request):
    if not request.method == 'POST':
        return process_response({'code': '002', 'msg': '请求方法错误'})
    else:
        # 数据经过中间件处理存放在 request.json_data 中
        json_data = request.json_data

        username = json_data['username']
        password = json_data['password']
        captcha = json_data['captcha']

        # 验证码 captcha 检验
        if request.session.get('captcha', '').lower() != captcha.lower():
            return process_response({'code': '004', 'msg': '验证码错误'})
        del request.session['captcha']

        # 用户 user 存在性验证
        user = account_models.User.objects.filter(username=username).first()
        if not user:
            return process_response({'code': '131', 'msg': '用户名错误'})

        # 密码 password 验证
        if check_password(password, user.password) is False:
            return process_response({'code': '132', 'msg': '密码错误'})

        # 设置登陆状态
        request.session['username'] = username

        return process_response({'code': '000', 'msg': '登陆成功'})
