from django.urls import path, include

from . import views


urlpatterns = [
    path('search/all_books/', views.book_search_list, name='book_list'),
]