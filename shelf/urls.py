from django.urls import path

from . import views


urlpatterns = [
    path('lists/', views.shelf_lists, name='shelf_lists'),
    path('add/<int:book_id>/', views.add_shelf_item, name='add_shelf_item'),
    path('update/<int:book_id>/<int:old_shelf_item_id>/', views.update_shelf_item, name='update_shelf_item'),
]
