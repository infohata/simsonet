from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from . import models, forms


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
    form_class = forms.FriendRequestCreateForm
    # fields = ('friend', 'request_message')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.info(self.request, f'{_("friend request sent to")} {form.instance.friend.username}')
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


def friend_request_accept(request, sender_id):
    friendship = get_object_or_404(models.Friend, user=sender_id, friend=request.user)
    if not friendship.is_accepted:
        friendship.is_accepted = True
        friendship.save()
        messages.success(request, f'{_("you are now friends with")} {friendship.user.username}')
    else:
        messages.warning(request, f'{_("you are already friends with")} {friendship.user.username}')
    return redirect(reverse_lazy('friend_list'))


def friend_block_unblock(request, sender_id):
    friendship = get_object_or_404(models.Friend, user=sender_id, friend=request.user)
    friendship.is_blocked = not friendship.is_blocked
    friendship.save()
    if friendship.is_blocked:
        messages.error(request, f'{_("you have blocked")} {friendship.user.username}')
    else:
        messages.success(request, f'{_("you have unblocked")} {friendship.user.username}')
    return redirect(reverse_lazy('friend_list'))
