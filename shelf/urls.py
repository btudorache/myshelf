from django.urls import path

from . import views


urlpatterns = [
    path('lists/', views.shelf_lists, name='shelf_lists'),
]
