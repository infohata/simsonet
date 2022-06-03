from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from . import models


class FriendListView(LoginRequiredMixin, generic.ListView):
    model = models.Friend
    template_name = 'simsonet_friends/friend_list.html'
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
    
