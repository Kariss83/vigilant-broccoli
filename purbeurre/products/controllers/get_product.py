from purbeurre.products.models import Products

class GetProductModule():
    def find_a_product_by_id(self, id):
        try :
            print(id)
            product = Products.objects.filter(id=id)
            print(product)
        except Exception :
            product = "produit introuvable"
        return product