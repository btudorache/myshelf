from django.urls import path

from . import views


urlpatterns = [
    path('lists/<int:user_id>/', views.shelf_lists, name='shelf_lists'),
    path('lists/row/<int:shelf_row_id>/', views.shelf_row_items, name='shelf_row_items'),
    path('add/<int:book_id>/', views.add_shelf_item, name='add_shelf_item'),
    path('add/shelf_row/', views.add_shelf, name='add_shelf_row'),
    path('update/<int:book_id>/<int:old_shelf_item_id>/', views.update_shelf_item, name='update_shelf_item'),
    path('delete/<int:shelf_item_id>/<section>/', views.delete_shelf_item, name='delete_shelf_item'),
    path('delete/<int:shelf_row_id>/', views.delete_shelf_row, name='delete_shelf_row'),
]
