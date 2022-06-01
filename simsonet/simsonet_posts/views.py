from django.contrib.auth import get_user_model, get_user
from django.shortcuts import get_object_or_404
from django.views import generic
from . models import Post, Wall


class WallDetailView(generic.DetailView):
    model = Wall
    template_name = 'simsonet_posts/wall.html'


class PostListView(generic.ListView):
    model = Post
    paginate_by = 20
    template_name = 'simsonet_posts/posts.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        wall_id = self.request.GET.get('wall_id')
        if wall_id:
            queryset = queryset.filter(wall=wall_id)
        owner_id = self.request.GET.get('owner_id')
        if owner_id:
            queryset = queryset.filter(owner=owner_id)
        else:
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
