""" This module is designed to host all the unit tests for parts of code
that are not views, models or forms.
"""
import random
from django.test import TestCase

from purbeurre.accounts.models import CustomUser
from purbeurre.products.models import Categories, Favorites, Products
from purbeurre.products.controllers.favorite_handling import (
    SaveFavoriteProductModule as SFP,
)
from purbeurre.products.controllers.favorite_handling import GetAllFavoriteModule as GAF
from purbeurre.products.controllers.get_product import GetProductModule as GP
from purbeurre.products.controllers.find_substitute import SearchModule


def create_an_user(number):
    user_test = CustomUser.objects.create(
        email=f"test{number}@gmail.com", name=f"MRTest{number}"
    )
    return user_test


def create_a_category(name):
    category = Categories.objects.create(name=name)
    return category


def create_a_product(number, nutri, category):
    prod = Products.objects.create(
        name=f"test{number}",
        url=f"http://test{number}.com",
        image=f"http://test{number}_image.com",
        nutriscore=nutri,
        energy=10,
        fat=10,
        saturated_fat=10,
        sugar=10,
        salt=10,
        category=category,
    )
    return prod


def create_a_favorite(user, searched_prod, replacement_prod):
    favorite = Favorites.objects.create(
        searched_product=searched_prod, substitution_product=replacement_prod, user=user
    )
    return favorite


class TestProductsModule(TestCase):
    """Main class testing all the actions the parser is supposed to be able to
    achieve.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.get(email="test1@gmail.com")
        cls.cat = create_a_category("Test")
        for i in range(10):
            create_a_product(i, random.choice(["a", "b", "c", "d", "e"]), cls.cat)

    def test_favorite_handler_can_save_favs(self):
        SFP.save_favorite_product(1, 1, 2)
        self.assertIsNotNone(Favorites.objects.all)

    def test_favorite_handler_returns_text_if_fail_saving(self):
        self.assertEqual(
            SFP.save_favorite_product(self.user.id + 1, 1, 2),
            "Impossible de sauvegarder le produit.",
        )

    def test_favorite_handler_can_retrieve_favs(self):
        prod1, prod2, prod3, prod4 = Products.objects.all()[:4]
        Favorites.objects.create(
            searched_product=prod1, substitution_product=prod2, user=self.user
        )
        Favorites.objects.create(
            searched_product=prod3, substitution_product=prod4, user=self.user
        )
        self.assertEqual(GAF.get_users_favorite(self.user.id).count(), 2)

    def test_favorite_handler_returns_text_if_fail_retrieving(self):
        self.assertEqual(
            GAF.get_users_favorite(self.user.id + 1),
            "Impossible de retourner vos favoris, veuillez rééssayer.",
        )

    def test_get_product_can_retrieve_a_given_object(self):
        prod = Products.objects.create(
            name="test",
            url="http://test.com",
            image="http://test_image.com",
            nutriscore="C",
            energy=10,
            fat=10,
            saturated_fat=10,
            sugar=10,
            salt=10,
            category=self.cat,
        )
        self.assertEqual(GP.find_a_product_by_id(prod.id), prod)

    def test_get_product_return_text_when_prod_not_found(self):
        ne_id = Products.objects.latest("id").id + 1
        self.assertEqual(GP.find_a_product_by_id(ne_id), "produit introuvable")

    def test_search_module_can_retrieve_substitutes(self):
        prod = Products.objects.all()[0]
        self.assertEqual(SearchModule.find_all_possible_substitute(prod)[1].count(), 6)

    def test_search_module_returns_right_text_when_not_found(self):
        self.assertEqual(
            SearchModule.find_all_possible_substitute("wrong_prod")[0],
            "produit introuvable",
        )
