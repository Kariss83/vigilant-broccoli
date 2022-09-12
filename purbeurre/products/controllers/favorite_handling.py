from purbeurre.products.models import Products, Favorites
from purbeurre.accounts.models import CustomUser


class SaveFavoriteProductModule:
    @staticmethod
    def save_favorite_product(user_id, product_id, searched_product_id):
        try:
            user = CustomUser.objects.filter(id=user_id)[0]
            product_to_save = Products.objects.filter(id=product_id)[0]
            searched_product = Products.objects.filter(id=searched_product_id)[0]
            Favorites.objects.get_or_create(
                searched_product=searched_product,
                substitution_product=product_to_save,
                user=user,
            )
        except Exception:
            message = "Impossible de sauvegarder le produit."
            return message


class GetAllFavoriteModule:
    @staticmethod
    def get_users_favorite(user_id):
        try:
            user = CustomUser.objects.filter(id=user_id)[0]
            favorites = Favorites.objects.filter(user=user)
            return favorites
        except Exception:
            message = "Impossible de retourner vos favoris, veuillez rééssayer."
            return message
