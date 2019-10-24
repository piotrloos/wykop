from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
#from django.utils.decorators import method_decorator
from django.views.generic import (DetailView, FormView, ListView, UpdateView,
                                  View)
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from wykop.accounts.forms import ConfirmTOSForm, RegisterForm
from wykop.accounts.models import User
from wykop.accounts.serializers import UserSerializer

#from wykop.settings import CURRENT_TOS


class LogoutRequiredMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse(settings.LOGIN_REDIRECT_URL))
        return super().dispatch(request, *args, **kwargs)

class RegisterView(LogoutRequiredMixin, FormView):
    form_class = RegisterForm
    template_name = 'user_register.html'

    def get_success_url(self):
        return reverse('posts:list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class UserLoginView(LogoutRequiredMixin, LoginView):
    template_name = 'user_login.html'

#    @method_decorator(user_passes_test(
#        lambda u: not u.is_authenticated,
#        reverse(settings.LOGIN_REDIRECT_URL)
#    ))
    
    # def get_success_url(self):
    #     return reverse('posts:list')

class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'

class UserDetailView(DetailView):
    model = User
    template_name = 'user_profile.html'
    context_object_name = 'author'

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user_update.html'
    fields = ('first_name', 'last_name', 'email')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('accounts:profile', args=(self.request.user.pk,))

class ConfirmTOSView(LoginRequiredMixin, FormView):
    template_name = 'user_tos.html'
    form_class = ConfirmTOSForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tos_version'] = settings.CURRENT_TOS
        return context

    def form_valid(self, form):
        user = self.request.user
        user.accepted_tos = settings.CURRENT_TOS
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        next = self.request.GET.get('next')
        if next:
            return next
        else:
            return reverse('posts:list')

class UserBanView(LoginRequiredMixin, View):

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        #if not request.user.is_staff:
        #    raise HTTP_403_FORBIDDEN

        user = get_object_or_404(User, pk=self.request.POST.get('user_id'))
        user.is_banned = self.request.POST.get('ban')
        user.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'], reverse('posts:list'))

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
