from rest_framework import routers

from wykop.accounts.views import UserViewSet
from wykop.posts.views import PostViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)