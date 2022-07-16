import random
from django.test import TestCase, Client

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions

from accounts.models import CustomUser
from products.models import Products, Categories, Favorites

opts = FirefoxOptions()
opts.add_argument("--headless")



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


class UserLoginTest(TestCase):

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

    def setUp(self):
        self.browser = webdriver.Firefox(options=opts)

    def test_can_login(self):
        self.browser.get('http://localhost:8000')

        h1text = self.browser.find_element(By.CSS_SELECTOR, '.text-white')
        self.assertTrue(h1text.is_displayed)
        self.assertIn('Purbeurre', self.browser.title)
        # self.assertIn('Du gras, oui, mais de qualité!', )
        self.browser.find_element(By.CLASS_NAME, "bi-person-plus").click()
        email = self.browser.find_element(By.ID, 'id_email')
        email.send_keys("test15@gmail.com")
        password = self.browser.find_element(By.ID, 'id_password')
        password.send_keys("monsupermotdepasse")
        submit_button = self.browser.find_element(By.CSS_SELECTOR, '.btn')
        submit_button.click()
        message = self.browser.find_element(By.CLASS_NAME, 'alert')
        self.assertIn('Vous êtes connecté(e)!', message.text)
        # user_id = CustomUser.objects.all()[0].id
        # self.client.get(reverse('home'), follow=True)
        # self.assertEqual(
        #     int(self.client.session['_auth_user_id']),
        #     user_id
        #     )

    def tearDown(self):
        self.browser.quit()


if __name__ == '__main__':
    pass
