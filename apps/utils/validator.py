import re


def validate_username(username: str) -> dict:
    """
    1. 长度大于等于 4
    2. 长度小于等于 20
    3. 仅含有字母、数字、下划线

    :param username: 用户名
    :return: 返回状态码
    """
    if len(username) < 4:
        return {'code': '102', 'msg': '用户名应不少于 4 位'}
    if len(username) > 20:
        return {'code': '103', 'msg': '用户名应不多于 20 位'}
    if re.search(r'[^A-Za-z0-9_]', username):
        return {'code': '104', 'msg': '用户名仅能含有字母、数字和下划线'}

    return {}


def validate_password(password: str) -> dict:
    """
        1. 长度大于等于 6
        2. 长度小于等于 20
        3. 仅含合法字符 ASCII 33 ~ 126
        4. 需含有数字
        5. 需含有字母

        :param password: 密码
        :return: 返回状态码
        """
    if len(password) < 6:
        return {'code': '112', 'msg': '密码应不少于 6 位'}
    if len(password) > 20:
        return {'code': '113', 'msg': '密码应不多于 20 位'}
    if not all(32 < ord(c) < 128 for c in password):
        return {'code': '114', 'msg': '密码应仅包含合法字符'}
    if not re.search(r'[0-9]', password):
        return {'code': '115', 'msg': '密码必须包含数字'}
    if not re.search(r'[A-Za-z]', password):
        return {'code': '116', 'msg': '密码必须包含字母'}

    return {}


def validate_email(email: str) -> dict:
    """
    1. 邮箱格式错误

    :param email: 邮箱
    :return: 返回状态码
    """
    if not re.search(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
        return {'code': '211', 'msg': '邮箱格式错误'}

    return {}
