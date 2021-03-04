
from selenium import webdriver

class Scraper(webdriver.Chrome):
    # def __init__(self):
    #     pass

    def login(self, config):
        self.get(config.get('urls', 'url_login'))
        self.find_element_by_id(config.get('login_controller', 'id')).send_keys(config.get('personal', 'id'))
        self.find_element_by_id(config.get('login_controller', 'pwd')).send_keys(config.get('personal', 'pwd'))
        self.find_element_by_id(config.get('login_controller', 'button')).click()

    def next_page(self):
        pass