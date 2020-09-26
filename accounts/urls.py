from django.urls import path, include

from . import views


urlpatterns = [
    path('profile/<username>/', views.user_detail, name='user_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
]
