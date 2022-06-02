from django.contrib.auth import get_user_model, get_user
from django.shortcuts import get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from . models import Post, Wall


class WallDetailView(generic.DetailView):
    model = Wall
    template_name = 'simsonet_posts/wall.html'


class PostListView(generic.ListView):
    model = Post
    paginate_by = 20
    template_name = 'simsonet_posts/post_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        wall_id = self.request.GET.get('wall_id')
        if wall_id:
            queryset = queryset.filter(wall=wall_id)
        owner_id = self.request.GET.get('owner_id')
        if owner_id:
            queryset = queryset.filter(owner=owner_id)
        elif not wall_id:
            queryset = queryset.filter(owner=get_user(self.request))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wall_id = self.request.GET.get('wall_id')
        if wall_id:
            context["wall"] = get_object_or_404(Wall, id=wall_id)
        owner_id = self.request.GET.get('owner_id')
        if owner_id:
            context["owner"] = get_object_or_404(get_user_model(), id=owner_id)
        else:
            context['owner'] = get_user(self.request)
        return context


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'simsonet_posts/post_detail.html'


class PostCreateView(generic.CreateView):
    model = Post
    template_name = 'simsonet_posts/post_create.html'
    fields = ('content', 'owner', 'wall', 'reply_to', 'repost_of', )

    def get_initial(self):
        initial = super().get_initial()
        initial['owner'] = self.request.user
        initial['wall'] = self.request.GET.get('wall_id')
        return initial

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
