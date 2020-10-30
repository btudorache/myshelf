from django import forms

from .models import ShelfItem, ShelfRow, Shelf


class ShelfItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ShelfItemForm, self).__init__(*args, **kwargs)
        self.fields['shelf_row'].queryset = Shelf.objects.get(owner=self.user).get_shelves()

    class Meta:
        model = ShelfItem
        fields = ('shelf_row',)


class ShelfRowForm(forms.ModelForm):
    class Meta:
        model = ShelfRow
        fields = ('name',)