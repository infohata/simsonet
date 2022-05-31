from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('view_profile/', views.view_my_profile, name='view_profile'),
    path('view_profile/<int:user_id>', views.view_user_profile, name='view_user_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
