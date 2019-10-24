from django.contrib.auth.views import LogoutView
from django.urls import path

from wykop.accounts.views import (ConfirmTOSView, RegisterView, UserBanView,
                                  UserDetailView, UserListView, UserLoginView,
                                  UserUpdateView)

app_name = 'accounts'

urlpatterns = [
    path('', UserListView.as_view(), name='list'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('<int:pk>', UserDetailView.as_view(), name='profile'),
    path('update', UserUpdateView.as_view(), name='update'),
    path('confirm', ConfirmTOSView.as_view(), name='confirm'),
    path('ban', UserBanView.as_view(), name='ban'),
]