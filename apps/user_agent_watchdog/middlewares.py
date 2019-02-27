from .models import UserAgentLog


class UserAgentLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            UserAgentLog.objects.create(user=request.user,
                                        user_agent=request.META['HTTP_USER_AGENT'])

        return self.get_response(request)
