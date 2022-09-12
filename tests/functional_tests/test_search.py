from django.test import Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions

from purbeurre.accounts.models import CustomUser

opts = FirefoxOptions()
opts.add_argument("--headless")


class SearchTest(StaticLiveServerTestCase):
    fixtures = [
        "/fixtures/dbdump.json",
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Firefox(options=opts)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_can_search_coca(self):
        self.selenium.get(f"{self.live_server_url}")

        search = self.selenium.find_element(
            By.CSS_SELECTOR, ".input-group > input:nth-child(1)"
        )
        search.send_keys("test0")
        submit_button = self.selenium.find_element(By.ID, "button-addon2")
        submit_button.click()
        results = self.selenium.find_element(By.CSS_SELECTOR, "#about")
        self.assertIn("test8", results.text)


if __name__ == "__main__":
    pass
