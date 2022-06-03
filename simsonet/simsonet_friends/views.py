from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from . import models


class FriendListView(LoginRequiredMixin, generic.ListView):
    model = models.Friend
    template_name = 'simsonet_friends/friend_list.html'
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.GET.get('user_id')
        if user_id:
            queryset = queryset.filter(user=user_id)
        else:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.GET.get('user_id')
        if user_id:
            context['user_'] = get_object_or_404(get_user_model(), id=user_id)
        context['friend_requests'] = models.Friend.objects.filter(friend=self.request.user, is_accepted=False)
        return context


class FriendRequestCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = models.Friend
    template_name = 'simsonet_friends/friend_request.html'
    success_url = reverse_lazy('friend_list')
    fields = ('friend', 'request_message')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial['friend'] = self.request.GET.get('friend_id')
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend'] = get_object_or_404(get_user_model(), id=self.request.GET.get('friend_id'))
        return context

    def test_func(self):
        friend_id = self.request.GET.get('friend_id')
        if not friend_id:
            return False
        friendship_found = models.Friend.objects.filter(user=self.request.user, friend=friend_id)
        if friendship_found:
            return False
        return not (self.request.user.id == int(friend_id))
