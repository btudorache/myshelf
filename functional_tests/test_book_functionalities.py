from .base import FunctionalTest

from time import sleep

class BookFunctionalitiesTest(FunctionalTest):
    def test_book_detail_functionalities(self):
        self.browser.get(self.live_server_url)

        # go to login page
        self.browser.find_element_by_id("login-button").click()

        # fill in login data
        self.browser.find_element_by_id("id_username").send_keys("opak")
        self.browser.find_element_by_id("id_password").send_keys("test")

        # login account
        self.browser.find_element_by_css_selector("input.btn.btn-primary").click()

        # go to book list
        self.browser.find_element_by_id("search-button").click()

        # find 5-th book on first page
        self.browser.find_element_by_id("button-5").click()

        # rate book
        self.browser.find_element_by_xpath('//*[@id="id_rate"]/option[4]').click()
        self.browser.find_element_by_id('rate-button').click()

        # write review
        self.browser.find_element_by_id('review-button').click()
        self.browser.find_element_by_css_selector('#id_text').send_keys('best book ever')
        self.browser.find_element_by_id('review-button').click()

        # add book to shelf
        self.browser.find_element_by_xpath('//*[@id="id_shelf_row"]/option[3]')
        self.browser.find_element_by_id('shelf-button').click()

