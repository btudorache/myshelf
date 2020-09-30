from django.urls import path

from . import views


urlpatterns = [
    path('search/all/', views.book_search_list, name='book_list'),
    path('search/<int:genre_id>/', views.book_search_list, name='book_list_by_genre'),
]
