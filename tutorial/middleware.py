from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse, reverse_lazy

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def exempturls(self, request):
        EXEMPT_URLS = [settings.LOGIN_URL.lstrip('/')]
        LOGIN_EXEMPT_URLS = (
            reverse_lazy("accounts:register"),  # register url - only logged out users see this
            reverse_lazy("accounts:reset_password"),  # next three are password reset urls - only logged out user
            reverse_lazy("accounts:password_reset_done"),  # see these.
            reverse_lazy("accounts:password_reset_complete"),
        )
        EXEMPT_URLS += [reverse_lazy(url) for url in settings.LOGIN_EXEMPT_URLS]

        return EXEMPT_URLS

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')

        url_is_exempt = self.exempturls(request)

        if path == reverse('accounts:logout').lstrip('/'):
            logout(request)

        if request.user.is_authenticated or url_is_exempt:
            return None

        else:
            return redirect(settings.LOGIN_REDIRECT_URL)
