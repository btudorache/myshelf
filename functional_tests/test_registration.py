from .base import FunctionalTest


class CreateAccountTest(FunctionalTest):
    def test_login(self):
        self.browser.get(self.live_server_url)

        # go to login page
        self.browser.find_element_by_id("login-button").click()

        # fill in login data
        self.browser.find_element_by_id("id_username").send_keys("opak")
        self.browser.find_element_by_id("id_password").send_keys("test")

        # login account
        self.browser.find_element_by_css_selector("input.btn.btn-primary").click()

    def test_create_account(self):
        self.browser.get(self.live_server_url)

        # go to register page
        self.browser.find_element_by_id("registration-button").click()

        # fill in registration data
        self.browser.find_element_by_id("id_username").send_keys("test_user10")
        self.browser.find_element_by_id("id_password").send_keys("testing1234")
        self.browser.find_element_by_id("id_password2").send_keys("testing1234")

        # finish registration
        self.browser.find_element_by_css_selector("input.btn.btn-primary").click()

        # go to login page
        self.browser.find_element_by_id("login-link").click()

        # fill in login data
        self.browser.find_element_by_id("id_username").send_keys("test_user10")
        self.browser.find_element_by_id("id_password").send_keys("testing1234")

        # login account
        self.browser.find_element_by_css_selector("input.btn.btn-primary").click()
