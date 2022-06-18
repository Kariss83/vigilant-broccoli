from django.test import TestCase, Client

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from purbeurre.accounts.models import CustomUser


opts = FirefoxOptions()
opts.add_argument("--headless")


def scroll_shim(passed_in_driver, object):
    x = object.location['x']
    y = object.location['y']
    scroll_by_coord = f'window.scrollTo({x},{y});'
    scroll_nav_out_of_way = 'window.scrollBy(0, -10);'
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)
    WebDriverWait(passed_in_driver, 20).until(EC.element_to_be_clickable((By.ID, "save_button")))


class FavoritesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.all().delete()
        cls.client = Client()
        cls.browser = webdriver.Firefox(options=opts)
        # cls.browser = webdriver.Chrome(options=opts)
        cls.browser.set_window_size(2400, 1000)

    def test_can_save_favorite(self):
        self.browser.get('http://localhost:8000')

        self.browser.find_element(By.CLASS_NAME, "bi-person-plus").click()
        username = self.browser.find_element_by_id('id_username')
        username.send_keys("test15@gmail.com")
        password = self.browser.find_element_by_id('id_password')
        password.send_keys("monsupermotdepasse")
        submit_button = self.browser.find_element_by_css_selector('.btn')
        submit_button.click()
        message = self.browser.find_element_by_class_name('alert')
        self.assertIn('Vous êtes connecté(e)!', message.text)

        search = self.browser.find_element_by_css_selector(
            '.input-group > input:nth-child(1)'
            )
        search.send_keys("coca")
        submit_button = self.browser.find_element_by_id('button-addon2')
        submit_button.click()
        results = self.browser.find_element_by_css_selector('#about')
        self.assertIn("Volvic", results.text)

        elements = self.browser.find_elements_by_id("save_button")
        scroll_shim(self.browser, elements[0])

        actions = ActionChains(self.browser)
        # actions.move_to_element(elements[0])
        actions.click()
        actions.perform()

        my_favs = self.browser.find_element_by_css_selector('.nav-link-with-img')
        my_favs.click()
        saved = self.browser.find_element_by_css_selector('div.col-lg-8:nth-child(1)')
        self.assertIn('Perrier', saved.text)

    def tearDown(self):
        self.browser.quit()


if __name__ == '__main__':
    pass
