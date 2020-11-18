from django.urls import path

from . import views


urlpatterns = [
    path('search/', views.book_search_list, name='book_list_search'),
    path('search/all/', views.book_search_list, name='book_list'),
    path('search/genre/<int:genre_id>/', views.book_search_list, name='book_list_by_genre'),
    path('search/author/<int:author_id>/', views.book_search_list, name='book_list_by_author'),
    path('search/<int:book_id>/', views.book_detail, name='book_detail'),
    path('rate/<int:book_id>/create/', views.book_rate_create, name='book_rate_create'),
    path('rate/<int:book_id>/<int:rating_id>/update/', views.book_rate_update, name='book_rate_update'),
    path('review/<int:review_id>/', views.book_review_detail, name='review_detail'),
    path('review/create/<book_title>/', views.book_create_review, name='review_book'),
    path('review/<book_title>/<int:review_id>/update/', views.book_update_review, name='update_book_review'),
]
