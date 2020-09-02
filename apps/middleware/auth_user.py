from django.utils.deprecation import MiddlewareMixin

from apps.utils.response_processor import process_response


class AuthUserMiddleware(MiddlewareMixin):
    LOGIN_REQUIRED_URL = {
        # TODO 临时不判断
        # '/api/account/user_info': ['POST'],
        #
        # '/api/comment/comment': ['POST']
    }

    def process_request(self, request):
        if request.path_info in self.LOGIN_REQUIRED_URL \
                and request.method in self.LOGIN_REQUIRED_URL[request.path_info]:
            if 'username' not in request.session:
                return process_response({'code': '006', 'msg': '未登陆'})
