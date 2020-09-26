from django.urls import path, include

from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
]
