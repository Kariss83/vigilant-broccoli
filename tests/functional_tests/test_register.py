import random

from django.test import Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions

from purbeurre.accounts.models import CustomUser

opts = FirefoxOptions()
opts.add_argument("--headless")


class UserCreationTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Firefox(options=opts)
        cls.selenium.implicitly_wait(10)
        CustomUser.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_can_register_a_new_account(self):
        self.selenium.get(f"{self.live_server_url}/users/register/")
        email = self.selenium.find_element(By.ID, "id_email")
        email.send_keys(f"test{random.randint(0,10000000000000000)}@gmail.com")
        name = self.selenium.find_element(By.ID, "id_name")
        name.send_keys("MRTest")
        password1 = self.selenium.find_element(By.ID, "id_password1")
        password1.send_keys("monsupermotdepasse")
        password2 = self.selenium.find_element(By.ID, "id_password2")
        password2.send_keys("monsupermotdepasse")
        submit_button = self.selenium.find_element(By.CSS_SELECTOR, ".btn")
        submit_button.click()
        message = self.selenium.find_element(By.CSS_SELECTOR, ".alert")
        self.assertIn("Vous êtes enregistré(e)...", message.text)
        profile_access = self.selenium.find_element(By.CSS_SELECTOR, ".bi-person")
        self.assertTrue(profile_access.is_displayed())


if __name__ == "__main__":
    pass
