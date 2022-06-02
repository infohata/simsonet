from django.urls import path
from . import views


urlpatterns = [
    path('wall/<int:pk>/', views.WallDetailView.as_view(), name='wall'),
    path('list/', views.PostListView.as_view(), name='post_list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
]
