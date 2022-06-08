""" This module is designed to host all the unit tests for the part of the
program in charge of parsing the sentence the user will pass to GrandPy.
"""
import random
from django.contrib import auth
from django.test import TestCase, Client
from django.urls import reverse
from purbeurre.accounts.forms import CustomAuthenticationForm

from purbeurre.accounts.models import CustomUser
from purbeurre.products.models import Categories, Favorites, Products


def create_an_user(number):
    user_test = CustomUser.objects.create(
            email=f"test{number}@gmail.com",
            name=f"MRTest{number}"
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
            category=category
            )
    return prod


def create_a_favorite(user, searched_prod, replacement_prod):
    favorite = Favorites.objects.create(
            searched_product=searched_prod,
            substitution_product=replacement_prod,
            user=user
            )
    return favorite


class TestAccountsViewsModule(TestCase):
    """ Main class testing all the actions the parser is supposed to be able to
    achieve.
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(
            email="test@gmail.com",
            name="MRTest",
        )
        cls.user.set_password('monsupermotdepasse')
        cls.user.save()

        cls.client = Client()

        cls.home_url = reverse('home')
        cls.register_url = reverse('register')
        cls.login_url = reverse('login')
        cls.logout_url = reverse('logout')
        cls.profile_url = reverse('profile')

    def test_login_user_GET(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    # def test_login_user_POST_fails_if_no_mail_or_password(self):
    #     response = self.client.post(
    #         self.login_url,
    #         {'username': '', 'password': 'monsupermotdepasse'},
    #         follow=True
    #         )
    #     self.assertRaises(KeyError, self.client.session, '_auth_user_id')
    #     self.assertEquals(response.status_code, 302)
    #     self.assertTrue(response.url.startswith('/login'))

    def test_login_user_POST(self):
        response = self.client.post(
            self.login_url,
            {'username': 'test@gmail.com', 'password': 'monsupermotdepasse'},
            )

        self.assertEqual(
            int(self.client.session['_auth_user_id']),
            self.user.id
            )
        self.assertEquals(response.status_code, 302)
        self.assertTrue(response.url.startswith('/'))

    def test_home_page_uses_item_form(self):
        response = self.client.post(self.login_url, follow=True)

        self.assertIsInstance(
            response.context['form'],
            CustomAuthenticationForm
            )

    def test_login_user_POST_invalid_form(self):
        form = CustomAuthenticationForm(
            data={
                'username': '',
                'password': 'monsupermotdepasse'
                }
            )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['username'],
            ["Ce champ est obligatoire."]
        )

    def test_register_user_GET(self):
        response = self.client.get(self.register_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register_user_POST(self):
        response = self.client.post(
            self.register_url,
            {'email': 'test2@gmail.com',
             'name': 'MRTest2',
             'password1': 'monsupermotdepasse',
             'password2': 'monsupermotdepasse'
             },
            follow=True
            )
        new_user = CustomUser.objects.get(name='MRTest2')
        self.assertEqual(
            int(self.client.session['_auth_user_id']),
            new_user.id
            )
        self.assertEquals(response.status_code, 200)  # why no redirection ?
        self.assertTemplateUsed(response, 'home/index.html')

    def test_register_user_POST_invalid_form(self):
        response = self.client.post(
            self.register_url,
            {'email': 'test2@gmail.com',
             'password1': 'monsupermotdepasse',
             },
            follow=True
            )
        # self.assertEquals(response.status_code, 200) # why no redirection ?
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Erreur de Création de Comptes - Veuillez reéssayer...')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_logout_user_GET(self):
        self.client.login(
            username='test@gmail.com',
            password='monsupermotdepasse'
            )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

        response = self.client.get(self.logout_url, follow=True)

        # self.assertFalse(user.is_authenticated)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Vous êtes déconnecté(e)...')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_profile_user_logged_in_GET(self):
        self.client.login(
            email='test@gmail.com',
            password='monsupermotdepasse'
            )
        # import pdb; pdb.set_trace()
        response = self.client.get(self.profile_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_profile_GET_while_not_logged_in(self):
        response = self.client.get(self.profile_url)

        self.assertEquals(response.status_code, 302)
        self.assertTrue(response.url.startswith('/registration/login/'))


class TestProductsViewsModule(TestCase):
    """ Main class testing all the actions the parser is supposed to be able to
    achieve.
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = create_an_user(1)
        cls.user.set_password('monsupermotdepasse')
        cls.user.save()
        cls.cat = create_a_category("Test")
        for i in range(10):
            create_a_product(i,
                             random.choice(["a", "b", "c", "d", "e"]),
                             cls.cat)
        cls.prod1, cls.prod2 = Products.objects.all()[:2]
        cls.fav1 = create_a_favorite(cls.user, cls.prod1, cls.prod2)

        cls.client = Client()

        cls.search_url = reverse('search')
        cls.savefavorite_url = reverse('savefavorite')
        cls.displayfavorite_url = reverse('displayfavorite')
        cls.product_url = reverse('product')

    def test_search_product_GET(self):
        response = self.client.get(self.search_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_search_product_POST(self):
        searched_prod = Products.objects.all()[0]
        response = self.client.post(
            self.search_url,
            {'searched': 'test0'},
            follow=True
            )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/search.html')
        self.assertTrue('searched_prod' in response.context)
        self.assertTrue('substitut_prods' in response.context)
        self.assertEqual(response.context['searched_prod'], searched_prod)
        self.assertEqual(len(response.context['substitut_prods']), 6)

    def test_info_product_GET(self):
        response = self.client.get(self.product_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/search.html')

    def test_info_product_POST(self):
        searched_prod = Products.objects.all()[0]
        response = self.client.post(
            self.product_url,
            {'prod_id': searched_prod.id},
            follow=True
            )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_info.html')
        self.assertTrue('product' in response.context)
        self.assertEqual(response.context['product'], searched_prod)

    def test_save_favorite_GET(self):
        self.client.login(
            email='test1@gmail.com',
            password='monsupermotdepasse'
            )
        response = self.client.get(self.savefavorite_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/search.html')

    def test_save_favorite_POST(self):
        self.client.login(
            email='test1@gmail.com',
            password='monsupermotdepasse'
            )
        searched_prod = Products.objects.all()[0]
        saved_prod = Products.objects.all()[5]
        response = self.client.post(
            self.savefavorite_url,
            {'favprod': saved_prod.id,
             'searched_prod_id': searched_prod.id,
             },
            follow=True
            )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/my_products.html')

        self.assertEqual(len(Favorites.objects.all()), 2)

    def test_show_favorite_GET(self):
        self.client.login(
            email='test1@gmail.com',
            password='monsupermotdepasse'
            )

        response = self.client.get(self.displayfavorite_url)

        self.assertEqual(str(response.context['user']), 'test1@gmail.com')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/my_products.html')
        self.assertTrue('favorites' in response.context)
        self.assertNotEqual(len(response.context['favorites']), 0)
        self.assertEqual(response.context['favorites'][0], self.fav1)
