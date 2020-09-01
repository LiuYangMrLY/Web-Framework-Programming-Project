from apps.account import models as account_models
from apps.comment import models as comment_models
from apps.utils.response_processor import process_response


def comment(request):
    if not request.method == "GET" and not request.method == "POST":
        return process_response({'code': '002', 'msg': '请求方法错误'})
    elif request.method == 'GET':
        return get_comments(request)
    else:
        return add_comment(request)


def get_comments(request):
    content = {'comments': []}

    comments = comment_models.Comment.objects.all()
    for one in comments:
        content['comments'].append({
            'username': one.user.username,
            'content': one.content,
            'time': one.create_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    content.update({'code': '000', 'msg': '获取成功'})
    return process_response(content)


def add_comment(request):
    if 'username' not in request.session:
        return process_response({'code': '006', 'msg': '无权限'})

    json_data = request.json_data

    content = json_data['content']
    if len(content) > 150:
        return process_response({'code': '142', 'msg': '评论过长'})

    user = account_models.User.objects.filter(username=request.session['username']).first()

    comm = comment_models.Comment(user=user, content=content)
    comm.save()

    return process_response({'code': '000', 'msg': '评论成功'})

