from configparser import ConfigParser, ExtendedInterpolation
import pickle
import time

from bs4 import BeautifulSoup
from selenium import webdriver

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read("okchundang.ini")


class Scraper(webdriver.Chrome):
    # def _init_(self, chrome, str):
    #     super(Scraper, self)._init_(chrome)
    #     self.config = ConfigParser(interpolation=ExtendedInterpolation())
    #     self.config.read(str)

    def proc(self):

    def login(self, config):
        self.get(config["urls"]["login"])
        self.find_element_by_id(config["login_controller"]["id"]).send_keys(
            config["login"]["id"]
        )
        self.find_element_by_id(config["login_controller"]["pwd"]).send_keys(
            config["login"]["pwd"]
        )
        self.find_element_by_id(config["login_controller"]["button"]).click()
        time.sleep(5)

    def to_formulas_page(self, config):
        self.switch_to.default_content()
        self.get(config["urls"]["formulas"])
        time.sleep(5)

    def to_next_page(self):
        next_page_button = self.find_element_by_css_selector(
            'a[title="Go to the next page"] > span'
        )
        next_page_button.click()
        time.sleep(3)

class tool:
    def __init__(self):
        self.dic_list = []
        # self.dic = {
        #     "formula_name": '',
        #     "formula_type": '',
        #     "formula_reference": '',
        #     "formula_recipe": {},
        #     "herbs_count": 0,
        #     "chub": '',
        # }

    def to_formula(self, tr) -> dict:
        div_list = tr.find_all("div")
        span_list = div_list[4].find('div').find_all('span', {'class': 'herb'})
        self.dic_list.append({
            "formula_name": div_list[4].text.split("\xa0")[0],
            "formula_type": div_list[1].text,
            "formula_reference": div_list[2].text,
            "formula_recipe": {
                    span.find_all("span")[0].text: span.find_all("span")[-1].text
                    for span in span_list
                              },
            "herbs_count": int(div_list[6].text),
            "chub": div_list[7].text.replace("\xa0", ""),
        })
        # self.dic["formular_name"] = div_list[4].text.split("\xa0")[0]

    def extract_data(table) -> list:
        # 출처가 다르거나 용량이 다른 '같은' 이름의 처방이 있기 때문에 리스트 형태로 해야 함.
        return [to_formula(tr) for tr in table.find_all("tr")[1:]]

    def data_from_page(page_source) -> list:
        return extract_data(BeautifulSoup(page_source, "html.parser").find_all("table")[-1])


def run():
    driver = Scraper("../chromedriver.exe", "okchundang.ini")
    driver.login(config)
    driver.to_formulas_page(config)

    whole_data = []
    a = 0

    while True:
        whole_data += data_from_page(driver.page_source)
        driver.to_next_page()
        a += 1
        if a >= 3:
            driver.close()
            break
    return whole_data


if __name__ == "__main__":
    whole_data = run()
    with open("ok_data.pickle", "wb") as file:
        pickle.dump(whole_data, file)
