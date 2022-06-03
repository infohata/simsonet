from django.shortcuts import render, redirect
from django.urls import reverse_lazy


def index(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('post_list')+'?wall_id='+str(request.user.walls.first().id))
    else:
        return redirect(reverse_lazy('login')+'?next='+reverse_lazy('index'))
