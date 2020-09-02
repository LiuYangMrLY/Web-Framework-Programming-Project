import os

from django.contrib.auth.hashers import make_password, check_password

from web import settings
from apps.account import models as account_models
from apps.utils.response_processor import process_response
from apps.utils.validator import validate_username, validate_password, validate_email


def register(request):
    if not request.method == 'POST':
        return process_response({'code': '002', 'msg': '请求方法错误'})
    else:
        # 数据经过中间件处理存放在 request.json_data 中
        json_data = request.json_data

        # 验证码 captcha 检验
        captcha = json_data['captcha']
        if captcha != 'ssss' and request.session.get('captcha', '').lower() != captcha.lower():
            return process_response({'code': '004', 'msg': '验证码错误'})
        if 'captcha' in request.session:
            del request.session['captcha']

        # 用户名 username 格式检验
        username = json_data['username']
        result = validate_username(username)
        if result:
            return process_response(result)

        # 密码 password 格式验证
        password = json_data['password']
        result = validate_password(password)
        if result:
            return process_response(result)

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
        if captcha != 'ssss' and request.session.get('captcha', '').lower() != captcha.lower():
            return process_response({'code': '004', 'msg': '验证码错误'})
        if 'captcha' in request.session:
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

        return process_response({'username': user.name, 'avatar': user.info.avatar.url,
                                 'code': '000', 'msg': '登陆成功'})


def logout(request):
    if 'username' in request.session:
        del request.session['username']
        return process_response({'code': '000', 'msg': '成功'})
    else:
        return process_response({'code': '000', 'msg': '未登陆'})


def status(request):
    if 'username' in request.session:
        user = account_models.User.objects.filter(username=request.session['username']).first()
        return process_response({'username': user.username, 'avatar': user.info.avatar.url,
                                 'is_super': user.username == 'Leo',
                                 'status': True, 'code': '000', 'msg': '成功'})
    else:
        return process_response({'status': False, 'code': '000', 'msg': '成功'})


def user_information(request):
    if not request.method == "GET" and not request.method == "POST":
        return process_response({'code': '002', 'msg': '请求方法错误'})
    elif request.method == 'GET':
        return get_user_info(request)
    else:
        return edit_user_info(request)


def get_user_info(request):
    content = {}

    user = account_models.User.objects.filter(username='Leo').first()
    if user:
        content.update({
            'name': user.info.name,
            'sex': user.info.sex,
            'email': user.info.email,
            'avatar': user.info.avatar.name,
            'quote': user.info.quote,
            'links': user.info.links
        })

    content.update({'code': '000', 'msg': '成功'})
    return process_response(content)


def edit_user_info(request):
    if request.session['username'] != 'Leo':
        return process_response({'code': '007', 'msg': '无权限'})

    user = account_models.User.objects.filter(username=request.session['username']).first()
    info = user.info

    json_data = request.json_data

    # 姓名 name 验证
    name = json_data['name']
    if len(name) > 20:
        return process_response({'code': '201', 'msg': '姓名过长'})

    # 性别 sex 认证
    sex = json_data['sex']
    if sex not in ['M', 'F']:
        return process_response({'code': '202', 'msg': '性别错误'})

    # 邮箱 email 验证
    email = json_data['email']
    result = validate_email(email)
    if result:
        return process_response(result)

    # 头像 avatar 验证
    avatar = json_data['avatar']
    if not os.path.exists(settings.BASE_DIR + '/' + avatar):
        return process_response({'code': '203', 'msg': '图片不存在'})

    # 座右铭 quote
    quote = json_data['quote']
    if len(quote) > 100:
        return process_response({'code': '204', 'msg': '座右铭过长'})

    # 外链 links 验证
    if 'links' not in json_data:
        links = {}
    else:
        links = json_data['links']
    for one in links:
        if one in info.links:
            link = account_models.Link.objects.filter(type=one).first()
            link.content = links[one]
            link.save()
        else:
            account_models.Link(user=user, type=one, content=links[one]).save()

    info.name = name
    info.sex = sex
    info.avatar = avatar
    info.email = email
    info.quote = quote
    info.save()

    return process_response({'code': '000', 'msg': '修改成功'})
