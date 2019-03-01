from .models import UserAgentLog


class UserAgentLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # This is processed AFTER getting response because of the fact that djangorestframework overrides request
        # live cycle and request.user is always anonymous here before calling `self.get_response`.
        # https://stackoverflow.com/questions/26240832/django-and-middleware-which-uses-request-user-is-always-anonymous
        if request.user.is_authenticated and 'HTTP_USER_AGENT' in request.META:
            UserAgentLog.objects.create(user=request.user,
                                        user_agent=request.META['HTTP_USER_AGENT'])

        return response
