from purbeurre.products.models import Products

class GetProductModule():
    def find_a_product_by_id(self, id):
        try :
            product = Products.objects.filter(id=id)
        except Exception :
            product = "produit introuvable"
        return product