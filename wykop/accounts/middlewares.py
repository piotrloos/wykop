from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

class TOSConfirmed:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        user = request.user
        if user.is_authenticated and user.accepted_tos < settings.CURRENT_TOS and request.path != reverse('accounts:confirm'):
            #return HttpResponseRedirect(reverse('accounts:confirm'))
            url = reverse('accounts:confirm') + '?next=' + request.path
            #print(url)
            return HttpResponseRedirect(url)
            #return redirect('accounts:confirm')

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response