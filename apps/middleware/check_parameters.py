from django.utils.deprecation import MiddlewareMixin

from apps.utils.response_processor import process_response


class CheckParametersMiddleware(MiddlewareMixin):
    URL_REQUIRED_PARAMETERS = {
        '/api/account/register': {
            'captcha': {'code': '003', 'msg': '缺少验证码'},
            'username': {'code': '101', 'msg': '缺少用户名'},
            'password': {'code': '111', 'msg': '缺少密码'}
        },

        '/api/account/login': {
            'captcha': {'code': '003', 'msg': '缺少验证码'},
            'username': {'code': '101', 'msg': '缺少用户名'},
            'password': {'code': '111', 'msg': '缺少密码'}
        }

    }

    def process_request(self, request):
        if request.method == 'POST' and request.path_info in self.URL_REQUIRED_PARAMETERS:
            parameters = self.URL_REQUIRED_PARAMETERS[request.path_info]

            for param in parameters:
                if param not in request.json_data or not request.json_data[param]:
                    return process_response(parameters[param])

