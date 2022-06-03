from django.urls import path
from . import views


urlpatterns = [
    path('list/', views.FriendListView.as_view(), name='friend_list'),
    # path('create/', views.PostCreateView.as_view(), name='post_create'),
    # path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    # path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    # path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]
