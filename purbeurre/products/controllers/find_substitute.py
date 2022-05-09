from purbeurre.products.models import  Products

class SearchModule():
    def find_all_possible_substitute(self, product):
        try :
            searched_product = Products.objects.filter(name__icontains=product)[0]
            print(searched_product)
            substit_list = Products.objects.filter(category_id=searched_product.category_id).order_by('nutriscore')[:6]
            print(substit_list)
            print(substit_list[0])
            print(substit_list[0].id)
            print(substit_list[0].nutriscore)
        except Exception :
            searched_product = "produit introuvable"
            substit_list = ''


        return searched_product, substit_list