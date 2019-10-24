from django.urls import path

from wykop.posts.views import (PostCreateView, PostDeleteView, PostDetailView,
                               PostListView, PostUpdateView, VoteView)

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('<int:pk>', PostDetailView.as_view(), name='details'),
    path('create', PostCreateView.as_view(), name='create'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='update'),
    path('vote/<int:post_pk>', VoteView.as_view(), name='vote'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='delete'),
]
