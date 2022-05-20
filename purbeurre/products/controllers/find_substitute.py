from purbeurre.products.models import  Products

class SearchModule():
    @staticmethod
    def find_all_possible_substitute(product):
        try :
            searched_product = Products.objects.filter(name__icontains=product)[0]
            substit_list = Products.objects.filter(category_id=searched_product.category_id).order_by('nutriscore')[:6]
        except Exception :
            searched_product = "produit introuvable"
            substit_list = ''
        return searched_product, substit_list