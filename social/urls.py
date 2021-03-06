from django.urls import path

from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('social/', views.user_list, name='user_list'),
    path('social/users/follow/<int:user_id>/', views.user_follow, name='user_follow'),
    path('social/users/unfollow/<int:user_id>/<int:contact_id>/', views.user_follow, name='user_unfollow'),
    path('social/<int:user_id>/', views.user_detail, name='social_user_detail'),
]
