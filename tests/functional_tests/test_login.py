from django.test import TestCase, Client

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions

from purbeurre.accounts.models import CustomUser

opts = FirefoxOptions()
opts.add_argument("--headless")


class UserLoginTest(TestCase):  

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

    def test_can_login(self):  
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        h1text = self.browser.find_element_by_css_selector('.text-white')
        self.assertTrue(h1text.is_displayed)
        self.assertIn('Purbeurre', self.browser.title) 
        # self.assertIn('Du gras, oui, mais de qualité!', )
        self.browser.find_element(By.CLASS_NAME, "bi-person-plus").click()
        username  = self.browser.find_element_by_id('id_username')
        username.send_keys("test15@gmail.com")
        password = self.browser.find_element_by_id('id_password')
        password.send_keys("monsupermotdepasse")
        submit_button = self.browser.find_element_by_css_selector('.btn')
        submit_button.click() 
        message = self.browser.find_element_by_class_name('alert')
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