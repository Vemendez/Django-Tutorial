from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse, reverse_lazy


class LoginRequiredMiddleware:

    def __init__(self, get_response):  # initialize class
        self.get_response = get_response

    def __call__(self, request):  # when browser sends request, get that request
        response = self.get_response(request)
        return response

    def exempturls(self, request):  # define the urls to check against when user is authenticate (or not)

        EXEMPT_URLS = () + (settings.LOGIN_URL.lstrip('/'),)  # login url from settings
        LOGIN_EXEMPT_URLS = (
            reverse_lazy("customers:register"),  # register url - only logged out users see this
            reverse_lazy("customers:reset_password"),  # next three are password reset urls - only logged out user
            reverse_lazy("customers:password_reset_done"),  # see these.
            reverse_lazy("customers:password_reset_complete"),
        )
        for i in LOGIN_EXEMPT_URLS:
            EXEMPT_URLS += (i.lstrip('/'),)  # make a tuple of all the urls that only logged out users see

        return EXEMPT_URLS  # return this tuple back to the class.

    def process_view(self, request, view_func, view_args, view_kwargs):  # process the view being requested.
        assert hasattr(request, 'user')  # make sure we have a request and get the user in that request (if any).
        path = request.path_info.lstrip('/')  # get the path in the request. Strip off the left '/'
        myexempturls = self.exempturls(request)  # call the exempturls function to get the tuple of exempt urls
        # we have on additional comparison to do. When reset_password (PasswordRestView) is called, it gets <uidb64>
        # and <token>. These may vary per request. They are obtained when the view is rendered. They do not appear to
        # be available when this middleware runs. A workaround is to take the left portion of the path string and
        # compare to the left portion of the url before the <uidb64> and <token> portions of the url. Doing this then
        # adds this reset_password/confirm (PasswordRestViewConfirm) call to the list of exempt urls, so that it can
        # be brought up when the user is logged out and resetting their password with the emailed link.
        if path in myexempturls or \
                path[0:len("customers/reset_password/confirm/")] == "customers/reset_password/confirm/":
            url_is_exempt = True
        else:
            url_is_exempt = False

        if path == reverse('customers:logout').lstrip('/'):
            logout(request)  # Make sure that if a user is logging out, they are allowed to do so.
        if (not request.user.is_authenticated and url_is_exempt) or \
                (request.user.is_authenticated and not url_is_exempt):
            return None  # Two conditions do not need special routing - logged out user trying an exempt url and
            # logged in user trying a non-exempt url.
        elif not request.user.is_authenticated and not url_is_exempt:
            return redirect(settings.LOGIN_URL)  # route to a login page if the user is not logged in and they are
            # trying a non-exempt url (only logged in users should see non-exempt urls).
        else:
            return redirect(settings.LOGIN_REDIRECT_URL)  # redirect to this setting url (currently profile page) if
            # the user is logged in and trying an exempt url (which only logged out users should see).
