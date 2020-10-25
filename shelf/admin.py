from django.contrib import admin
from .models import Shelf, ShelfRow, ShelfItem


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ['owner']


@admin.register(ShelfRow)
class ShelfRowAdmin(admin.ModelAdmin):
    list_display = ['name', 'shelf']


@admin.register(ShelfItem)
class ShelfItemAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'shelf_row', 'book', ]

