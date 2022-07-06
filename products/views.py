# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from products.controllers.find_substitute import SearchModule
from products.controllers.get_product import GetProductModule
from products.controllers.favorite_handling import SaveFavoriteProductModule
from products.controllers.favorite_handling import GetAllFavoriteModule


def search_product(request):
    # import pdb; pdb.set_trace()
    if request.method == "POST":
        searched = request.POST['searched']
        search_module = SearchModule()
        substit = search_module.find_all_possible_substitute(searched)
        context = {'searched_prod': substit[0],
                   'substitut_prods': substit[1]}
        return render(request, 'search/search.html', context)
    else:
        return render(request, 'home/index.html', {})


def info_product(request):
    """ Return the information about the selected product. """
    # import pdb; pdb.set_trace()

    if request.method == "POST":
        prod_id = request.POST.get('prod_id', None)
        get_prod_module = GetProductModule()
        product = get_prod_module.find_a_product_by_id(prod_id)
        context = {'product': product}
        return render(request, 'products/product_info.html', context)
    else:
        return render(request, 'search/search.html', {})


@login_required
def save_favorite(request):
    if request.method == "POST":
        saver = SaveFavoriteProductModule()
        user_id = request.user.id
        substitut_id = request.POST.get('favprod', None)
        searched_id = request.POST.get('searched_prod_id', None)
        saver.save_favorite_product(user_id, searched_id, substitut_id)
        return redirect('/products/favorites/')
    else:
        return render(request, 'search/search.html', {})


@login_required
def show_favorite(request):
    data_handler = GetAllFavoriteModule()
    user_id = request.user.id
    favorites = data_handler.get_users_favorite(user_id)
    context = {'favorites': favorites}
    return render(request, 'products/my_products.html', context)
