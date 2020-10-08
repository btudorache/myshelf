from django.urls import path

from . import views


urlpatterns = [
    path('search/', views.book_search_list, name='book_list_search'),
    path('search/all/', views.book_search_list, name='book_list'),
    path('search/genre/<int:genre_id>/', views.book_search_list, name='book_list_by_genre'),
    path('search/author/<int:author_id>/', views.book_search_list, name='book_list_by_author'),
    path('search/<int:book_id>/', views.book_detail, name='book_detail'),
]
