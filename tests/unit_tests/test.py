""" This module is designed to host all the unit tests for the part of the
program in charge of parsing the sentence the user will pass to GrandPy.
"""
from django.test import TestCase

from purbeurre.accounts.models import CustomUser
from purbeurre.products.models import  Categories, Favorites, Products
from purbeurre.products.controllers.favorite_handling import SaveFavoriteProductModule as SFP
from purbeurre.products.controllers.favorite_handling import GetAllFavoriteModule as GAF
from purbeurre.products.controllers.get_product import GetProductModule as GP
from purbeurre.products.controllers.find_substitute import SearchModule


def create_an_user(number):
    user_test = CustomUser.objects.create(
            email = f"test{number}@gmail.com",
            name = f"MRTest{number}"
        )
    return user_test

def create_a_category(name):
    category = Categories.objects.create(name=name)
    return category

def create_a_product(number,nutri, category):
    prod = Products.objects.create(
            name = f"test{number}", 
            url = f"http://test{number}.com",
            image = f"http://test{number}_image.com",
            nutriscore = nutri,
            energy = 10,
            fat = 10,
            saturated_fat = 10,
            sugar = 10,
            salt = 10,
            category = category
            )
    return prod

def create_a_favorite(user, searched_prod, replacement_prod):
    favorite = Favorites.objects.create(
            searched_product = searched_prod,
            substitution_product = replacement_prod, 
            user = user
            )
    return favorite
    

class TestAccountsModule(TestCase):
    """ Main class testing all the actions the parser is supposed to be able to 
    achieve.
    """   
    def test_(self):
        pass
        

class TestProductsModule(TestCase):
    """ Main class testing all the actions the parser is supposed to be able to 
    achieve.
    """
    def test_favorite_handler_can_save_favs(self):
        create_an_user(1)
        category = create_a_category("Test")
        create_a_product(1, "B", category)
        create_a_product(2, "A", category)
        SFP.save_favorite_product(1, 1, 2)
        self.assertNotEqual(Favorites.objects.all, None)

    def test_favorite_handler_can_retrieve_favs(self):
        user_test = create_an_user(1)
        category = create_a_category("test")
        prod1 = create_a_product(1, "B", category)
        prod2 = create_a_product(2, "A", category)
        prod3 = create_a_product(3, "B", category)
        prod4 = create_a_product(4, "A", category)
        Favorites.objects.create(
            searched_product = prod1,
            substitution_product = prod2, 
            user = user_test
            )
        Favorites.objects.create(
            searched_product = prod3,
            substitution_product = prod4, 
            user = user_test
            )
        self.assertEqual(GAF.get_users_favorite(1).count(), 2)

    def test_get_product_can_retrieve_a_given_object(self):
        category = create_a_category("Test")
        prod5 = create_a_product(5, "A", category)
        # import pdb; pdb.set_trace()
        self.assertEqual(GP.find_a_product_by_id(7), prod5)
    
    def test_get_product_return_text_when_prod_not_found(self):
        self.assertEqual(GP.find_a_product_by_id(10), "produit introuvable")

    def test_search_module_can_retrieve_substitutes(self):
        category = create_a_category("test")
        prod = create_a_product(10, "B", category)
        create_a_product(1, "B", category)
        create_a_product(2, "A", category)
        create_a_product(3, "B", category)
        create_a_product(4, "A", category)
        create_a_product(5, "B", category)
        create_a_product(6, "A", category)
        create_a_product(7, "B", category)
        create_a_product(8, "A", category)
        self.assertEqual(
            SearchModule.find_all_possible_substitute(prod)[1].count(),
            6)
    
    def test_search_module_returns_right_text_when_not_found(self):
        self.assertEqual(
            SearchModule.find_all_possible_substitute("wrong_prod")[0],
            "produit introuvable")


class TestHomeModule(TestCase):
    """ Main class testing all the actions the parser is supposed to be able to 
    achieve.
    """
    def test_search_module_return_highest_nutriscore(self):
        pass