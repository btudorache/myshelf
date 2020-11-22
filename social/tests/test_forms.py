from django.test import TestCase

from ..forms import SearchForm


class SearchFormTest(TestCase):
    def test_search_form(self):
        form = SearchForm(data={'query': 'user1'})
        self.assertEquals(form.is_valid(), True)
        self.assertEquals(form.cleaned_data['query'], 'user1')