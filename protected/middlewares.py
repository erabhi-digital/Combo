#pip install django-axes

BLOCKED_AGENTS = [
    'Scrapy',
    'python-requests',
    'curl',
    'wget'
]

class BlockBotsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ua = request.META.get('HTTP_USER_AGENT', '')
        if any(bot in ua for bot in BLOCKED_AGENTS):
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden()
        return self.get_response(request)