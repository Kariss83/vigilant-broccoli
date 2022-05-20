from django.test import TestCase, Client

from selenium import webdriver
from selenium.webdriver import FirefoxOptions

from purbeurre.accounts.models import CustomUser

opts = FirefoxOptions()
opts.add_argument("--headless")


class SearchTest(TestCase):  

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(
            email = "test_test@gmail.com",
            name = "MRTest"
        )
        cls.user.set_password('monsupermotdepasse')
        cls.user.save()

        cls.client = Client()

    def setUp(self):
        self.browser = webdriver.Firefox(options=opts)        

    def test_can_search_coca(self):  
        self.browser.get('http://localhost:8000')

        search  = self.browser.find_element_by_css_selector(
            '.input-group > input:nth-child(1)'
            )
        search.send_keys("coca")
        submit_button = self.browser.find_element_by_id('button-addon2')
        submit_button.click() 
        results = self.browser.find_element_by_css_selector('#about')
        self.assertIn("Volvic", results.text)


    def tearDown(self):  
        self.browser.quit()

if __name__ == '__main__':  
    pass