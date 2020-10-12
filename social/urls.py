from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('social/', views.user_list, name='user_list'),
    path('social/<int:user_id>', views.user_detail, name='social_user_detail'),
]
