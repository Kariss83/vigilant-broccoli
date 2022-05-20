import random

from django.test import TestCase, Client
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver import FirefoxOptions

from purbeurre.accounts.models import CustomUser

opts = FirefoxOptions()
opts.add_argument("--headless")


class UserCreationTest(TestCase):  

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.all().delete()
        cls.client = Client()
        cls.browser = webdriver.Firefox(options=opts) 

    def test_can_register_a_new_account(self):  
        self.browser.get('http://localhost:8000/register/')
        email  = self.browser.find_element_by_id('id_email')
        email.send_keys(f"test{random.randint(0,10000000000000000)}@gmail.com")
        name = self.browser.find_element_by_id('id_name')
        name.send_keys("MRTest")
        password1 = self.browser.find_element_by_id('id_password1')
        password1.send_keys("monsupermotdepasse")
        password2 = self.browser.find_element_by_id('id_password2')
        password2.send_keys("monsupermotdepasse")
        submit_button = self.browser.find_element_by_css_selector('.btn')
        submit_button.click() 
        message = self.browser.find_element_by_css_selector('.alert')
        # import pdb; pdb.set_trace()
        self.assertIn('Vous êtes enregistré(e)...', message.text)
        profile_access = self.browser.find_element_by_css_selector('.bi-person')
        self.assertTrue(profile_access.is_displayed())


    def tearDown(self):  
        self.browser.quit()

if __name__ == '__main__':  
    pass