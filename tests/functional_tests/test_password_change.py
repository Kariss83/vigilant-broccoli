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

    def test_can_register_logout_reset_password_request(self):
        # account creation
        self.browser.get('http://localhost:8000/users/register/')
        random_number = random.randint(0,10000000000000000)
        email = self.browser.find_element(By.ID, 'id_email')
        email.send_keys(f"test{random_number}@gmail.com")
        name = self.browser.find_element(By.ID, 'id_name')
        name.send_keys("MRTest")
        password1 = self.browser.find_element(By.ID, 'id_password1')
        password1.send_keys("monsupermotdepasse")
        password2 = self.browser.find_element(By.ID, 'id_password2')
        password2.send_keys("monsupermotdepasse")
        submit_button = self.browser.find_element(By.CSS_SELECTOR, '.btn')
        submit_button.click()
        message = self.browser.find_element(By.CSS_SELECTOR, '.alert')
        self.assertIn('Vous êtes enregistré(e)...', message.text)

        # account logout
        self.browser.get('http://localhost:8000/users/logout/')
        message = self.browser.find_element(By.CSS_SELECTOR, '.alert')
        self.assertIn('Vous êtes déconnecté(e)...', message.text)

        # asking a password reset
        self.browser.get('http://127.0.0.1:8000/users/login/')
        link = self.browser.find_element(
            By.CSS_SELECTOR,
            '.offset-md-3 > form:nth-child(1) > div:nth-child(5) > p:nth-child(1) > a:nth-child(1)'
            )
        link.click()
        email_input = self.browser.find_element(By.ID, 'id_email')
        email_input.send_keys(f"test{random_number}@gmail.com")
        submit_button = self.browser.find_element(By.CSS_SELECTOR, '.btn')
        submit_button.click()
        
        # checking for email message
        message = self.browser.find_element(By.CSS_SELECTOR, '.alert')
        self.assertIn(
            'Un message contenant les instructions de réinitialisation vous a été envoyé.',
            message.text
            )


    def tearDown(self):
        self.browser.quit()


if __name__ == '__main__':
    pass