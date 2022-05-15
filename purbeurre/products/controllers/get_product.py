from purbeurre.products.models import Products

class GetProductModule():
    @staticmethod
    def find_a_product_by_id(id):
        try :
            product = Products.objects.get(id=id)
        except Exception :
            product = "produit introuvable"
        return product