from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import TemplateView

from purbeurre.products.controllers.find_substitute import SearchModule

# Create your views here.
# class SearchView(TemplateView):
#     template_name = 'search/search.html'

#     def get_context_data(self, **kwargs):
#         search_module = SearchModule()
#         substit = search_module.find_all_possible_substitute("coca")
#         context = super().get_context_data(**kwargs)
#         context['searched_prod'] = substit[0]
#         context['substitut_prods'] = substit[1]
#         return context 
    
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             # <process form cleaned data>
#             return HttpResponseRedirect('/success/')

#         return render(request, self.template_name, {'form': form})

def search_product(request):
    if request.method == "POST":
        searched = request.POST['searched']
        search_module = SearchModule()
        substit = search_module.find_all_possible_substitute(searched)
        context = {'searched_prod': substit[0],
                   'substitut_prods': substit[1]}
        return render(request, 'search/search.html', context)
    else :
        return render(request, 'search/search.html', {})

