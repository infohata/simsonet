from django.urls import path
from . import views


urlpatterns = [
    path('wall/<int:pk>/', views.WallDetailView.as_view(), name='wall'),
    path('list/', views.PostListView.as_view(), name='post_list'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('api/list/', views.PostListCreateAPI.as_view()),
    path('api/<int:pk>/', views.PostDetailUpdateDeleteAPI.as_view()),
    path('api/<int:pk>/replies/', views.PostReplyListCreateAPI.as_view()),
    path('api/<int:pk>/like/', views.LikeCreateAPIView.as_view()),
]
