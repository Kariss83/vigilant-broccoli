from django.test import Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

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
    x = object.location["x"]
    y = object.location["y"]
    scroll_by_coord = f"window.scrollTo({x},{y});"
    scroll_nav_out_of_way = "window.scrollBy(0, -10);"
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)
    WebDriverWait(passed_in_driver, 20).until(
        EC.element_to_be_clickable((By.ID, "save_button"))
    )


def create_an_user(number):
    user_test = CustomUser.objects.create(
        email=f"test{number}@gmail.com", name=f"MRTest{number}"
    )
    return user_test


class FavoritesTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Firefox(options=opts)
        cls.selenium.implicitly_wait(10)
        cls.selenium.set_window_size(2400, 1000)
        cls.user = create_an_user(1)
        cls.user.set_password("monsupermotdepasse")
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_can_save_favorite(self):
        self.selenium.get(f"{self.live_server_url}")

        self.selenium.find_element(By.CLASS_NAME, "bi-person-plus").click()
        username = self.selenium.find_element(By.ID, "id_email")
        username.send_keys("test1@gmail.com")
        password = self.selenium.find_element(By.ID, "id_password")
        password.send_keys("monsupermotdepasse")
        submit_button = self.selenium.find_element(By.CSS_SELECTOR, ".btn")
        submit_button.click()
        message = self.selenium.find_element(By.CLASS_NAME, "alert")
        self.assertIn("Vous êtes connecté(e)!", message.text)

        search = self.selenium.find_element(
            By.CSS_SELECTOR, ".input-group > input:nth-child(1)"
        )
        search.send_keys("test0")
        submit_button = self.selenium.find_element(By.ID, "button-addon2")
        submit_button.click()
        results = self.selenium.find_element(By.CSS_SELECTOR, "#about")
        self.assertIn("test8", results.text)

        elements = self.selenium.find_elements(By.ID, "save_button")
        scroll_shim(self.selenium, elements[1])

        actions = ActionChains(self.selenium)
        actions.click()
        actions.perform()

        saved = self.selenium.find_element(By.CSS_SELECTOR, "#page-top > header")
        self.assertIn("test0", saved.text)


if __name__ == "__main__":
    pass
