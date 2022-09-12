import random
from django.test import Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions

from purbeurre.accounts.models import CustomUser
from purbeurre.products.models import Products, Categories, Favorites

opts = FirefoxOptions()
opts.add_argument("--headless")


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


class UserLoginTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Firefox(options=opts)
        cls.selenium.implicitly_wait(10)

        # cls.user = create_an_user(1)
        # cls.user.set_password("monsupermotdepasse")
        # cls.user.save()
        cls.user = CustomUser.objects.get(email="test1@gmail.com")

        cls.cat = create_a_category("Test")

        for i in range(10):
            create_a_product(i, random.choice(["a", "b", "c", "d", "e"]), cls.cat)

        cls.prod1, cls.prod2 = Products.objects.all()[:2]

        cls.fav1 = Favorites.objects.get(
            user=cls.user, searched_product=cls.prod1, substitution_product=cls.prod2
        )
        # create_a_favorite(cls.user, cls.prod1, cls.prod2)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_can_login_then_modify_name(self):
        self.selenium.get(f"{self.live_server_url}")

        h1text = self.selenium.find_element(By.CSS_SELECTOR, ".text-white")
        self.assertTrue(h1text.is_displayed)
        self.assertIn("Purbeurre", self.selenium.title)
        # self.assertIn('Du gras, oui, mais de qualité!', )
        self.selenium.find_element(By.CLASS_NAME, "bi-person-plus").click()
        username = self.selenium.find_element(By.ID, "id_email")
        username.send_keys("test1@gmail.com")
        password = self.selenium.find_element(By.ID, "id_password")
        password.send_keys("monsupermotdepasse")
        submit_button = self.selenium.find_element(By.CSS_SELECTOR, ".btn")
        submit_button.click()
        message = self.selenium.find_element(By.CLASS_NAME, "alert")
        self.assertIn("Vous êtes connecté(e)!", message.text)
        self.selenium.find_element(By.CLASS_NAME, "bi-person").click()
        self.selenium.find_element(
            By.CSS_SELECTOR, ".col-lg-8 > a:nth-child(8)"
        ).click()
        name = self.selenium.find_element(By.ID, "id_name")
        name.clear()
        name.send_keys("MissTest")
        submit_button = self.selenium.find_element(By.CSS_SELECTOR, ".btn")
        submit_button.click()
        message = self.selenium.find_element(By.CLASS_NAME, "alert")
        self.assertIn("Modifications enregistrées avec succès.", message.text)
        new_name = self.selenium.find_element(
            By.CSS_SELECTOR, "h2.text-white-75:nth-child(3)"
        )
        self.assertEqual(new_name.text, "MissTest")


if __name__ == "__main__":
    pass
