#from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView, View)
from requests.api import request
from rest_framework import viewsets
from rest_framework.status import HTTP_403_FORBIDDEN

from wykop.posts.models import Post, Vote
from wykop.posts.permissions import IsOwnerOrReadOnly
from wykop.posts.serializers import PostSerializer

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = '-created'
    paginate_by = 3
#   queryset = Post.objects.filter(votes__gte=0)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_value'] = self.request.GET.get('search') or ''
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        # qs = Post.objects.all().order_by('-votes')
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(text__icontains=search))
        return qs

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_details.html'
    context_object_name = 'post'

    # stare rozwiązanie - obliczające prev/next w pythonie

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     posts_ids = list(Post.objects.order_by('-votes').values_list('pk', flat=True))
    #     cur_post_index = posts_ids.index(self.get_object().pk)
    #     if cur_post_index+1 < len(posts_ids):
    #         context["next_post_id"] = posts_ids[cur_post_index+1]
    #     else:
    #         context["next_post_id"] = None
    #     if cur_post_index-1 >= 0:
    #         context["prev_post_id"] = posts_ids[cur_post_index-1]
    #     else:
    #         context["prev_post_id"] = None
    #     return context

    # nowe rozwiązanie - obliczające prev/next w bazie danych (na querysecie)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cur_qs = Post.objects.order_by('-created')
        cur_created = self.get_object().created

        context['next_post'] = cur_qs.filter(created__lt=cur_created).first()
        context['prev_post'] = cur_qs.filter(created__gt=cur_created).last()

        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = ['title', 'text', 'image', 'video']

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_banned:
            return HttpResponseForbidden(reverse('posts:list'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title', 'text', 'image', 'video']

    def get_queryset(self):
        return super().get_queryset().filter(author_id=self.request.user.pk)

class VoteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        #post = get_object_or_404(Post, pk=kwargs['post_pk'])

        post = Post.objects.get(pk=kwargs['post_pk'])
        if post.author_id == request.user.pk:
            raise HTTP_403_FORBIDDEN

        Vote.objects.create(
            post=post,
            user=request.user,
            value=request.POST['value']
        )

        return HttpResponseRedirect(request.META['HTTP_REFERER'])

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts:list')
    template_name = 'post_check_delete.html'

    def get_queryset(self):
        return super().get_queryset().filter(author_id=self.request.user.pk)

# ViewSets define the view behavior.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)