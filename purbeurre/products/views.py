from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import TemplateView

from purbeurre.products.controllers.find_substitute import SearchModule

# Create your views here.
class SearchView(TemplateView):
    template_name = 'search/search.html'

    def get_context_data(self, **kwargs):
        search_module = SearchModule()
        substit = search_module.find_all_possible_substitute("coca")
        context = super().get_context_data(**kwargs)
        context['searched_prod'] = substit[0]
        context['substitut_prods'] = substit[1]
        return context 

