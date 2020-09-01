import json

from django.utils.deprecation import MiddlewareMixin

from apps.utils.response_processor import process_response


class ValidateJSONMiddleware(MiddlewareMixin):
    JSON_USED_URL = [
        '/api/account/register',
        '/api/account/login'
    ]

    def process_request(self, request):
        if request.method == 'POST' and request.path_info in self.JSON_USED_URL:
            # JSON 格式检验
            try:
                json_data = json.loads(request.body)
                request.json_data = json_data
            except json.JSONDecodeError:
                json_data = {}
            if not json_data:
                return process_response({'code': '0001', 'msg': 'JSON 格式解析错误'})
