from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from rest_framework import generics, permissions, exceptions, mixins, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from . forms import PostForm
from . models import Post, Wall, Like
from . serializers import PostSerializer, LikeSerializer


class WallDetailView(generic.DetailView):
    model = Wall
    template_name = 'simsonet_posts/wall.html'


class PostListView(generic.ListView):
    model = Post
    paginate_by = 10
    template_name = 'simsonet_posts/post_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        wall_id = self.request.GET.get('wall_id')
        if wall_id:
            queryset = queryset.filter(wall=wall_id)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(content__icontains=search) |
                Q(owner__username__icontains=search) |
                Q(owner__first_name__in=search.split(), owner__last_name__in=search.split())
            )
        owner_id = self.request.GET.get('owner_id')
        if owner_id:
            queryset = queryset.filter(owner=owner_id)
        elif not wall_id:
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and not hasattr(self.request.user, 'auth_token'):
            Token(user=self.request.user).save()
        wall_id = self.request.GET.get('wall_id')
        if wall_id:
            context["wall"] = get_object_or_404(Wall, id=wall_id)
        owner_id = self.request.GET.get('owner_id')
        if owner_id:
            context["owner"] = get_object_or_404(get_user_model(), id=owner_id)
        else:
            context['owner'] = self.request.user
        return context


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'simsonet_posts/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and not hasattr(self.request.user, 'auth_token'):
            Token(user=self.request.user).save()
        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = 'simsonet_posts/post_create.html'
    form_class = PostForm

    def get_initial(self):
        initial = super().get_initial()
        initial['owner'] = self.request.user
        initial['wall'] = self.request.GET.get('wall_id')
        initial['reply_to'] = self.request.GET.get('reply_to')
        initial['repost_of'] = self.request.GET.get('repost_of')
        if initial['repost_of'] and not initial['wall']:
            initial['wall'] = self.request.user.walls.first()
        return initial

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, _('Posted successfully'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wall_id = self.request.GET.get('wall_id')
        if wall_id:
            context["wall"] = get_object_or_404(Wall, id=wall_id)
        reply_to = self.request.GET.get('reply_to')
        if reply_to:
            context["reply_to"] = get_object_or_404(Post, id=reply_to)
        repost_of = self.request.GET.get('repost_of')
        if repost_of:
            context["repost_of"] = get_object_or_404(Post, id=repost_of)
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    template_name = 'simsonet_posts/post_update.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.id = self.get_object().id
        form.instance.owner = self.request.user
        messages.success(self.request, _('Updated successfully'))
        return super().form_valid(form)

    def test_func(self):
        post_instance = self.get_object()
        return post_instance.owner == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = 'simsonet_posts/post_delete.html'

    def test_func(self):
        post_instance = self.get_object()
        return post_instance.owner == self.request.user

    def get_success_url(self):
        messages.success(self.request, _('Deleted successfully'))
        return reverse_lazy('post_list')+'?wall_id='+str(self.request.user.walls.first().id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete'] = True
        return context


class PostListCreateAPI(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.data.get('reply_to'):
            serializer.save(owner=self.request.user, wall=None)
        serializer.save(owner=self.request.user)


class PostDetailUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], owner=self.request.user)
        if post.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise exceptions.ValidationError(_('you cannot edit posts of other users'.capitalize()))

    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], owner=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise exceptions.ValidationError(_('you cannot delete posts of other users'.capitalize()))


class PostReplyListCreateAPI(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(reply_to=self.kwargs['pk'])

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs['pk'])
        serializer.save(owner=self.request.user, wall=None, reply_to=post)


class LikeCreateAPIView(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Like.objects.filter(owner=self.request.user, post=post)

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['pk'])
        if self.get_queryset().exists():
            raise exceptions.ValidationError(_('you already liked this post').capitalize())
        else:
            serializer.save(owner=self.request.user, post=post)

    def delete(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise exceptions.ValidationError(_('you did not leave a like to this post yet').capitalize())
