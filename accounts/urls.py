from django.urls import path, include

from . import views


urlpatterns = [
    path('profile/', views.user_detail, name='user_profile'),
    path('profile/update', views.update_user, name='update_profile'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
]
