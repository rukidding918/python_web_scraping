from configparser import ConfigParser, ExtendedInterpolation
import pickle
import time

from bs4 import BeautifulSoup
from selenium import webdriver


class Scraper(webdriver.Chrome):
    def __init__(self, executable_path, config_path):
        super(Scraper, self).__init__(executable_path)
        self.config = ConfigParser(interpolation=ExtendedInterpolation())
        self.config.read(config_path)

    def login(self):
        self.get(self.config["urls"]["login"])
        self.find_element_by_id(self.config["login_controller"]["id"]).send_keys(
            self.config["login"]["id"]
        )
        self.find_element_by_id(self.config["login_controller"]["pwd"]).send_keys(
            self.config["login"]["pwd"]
        )
        self.find_element_by_id(self.config["login_controller"]["button"]).click()
        time.sleep(5)

    def to_formulas_page(self):
        self.switch_to.default_content()
        self.get(self.config["urls"]["formulas"])
        time.sleep(5)

    def to_next_page_or_finish(self):
        next_page_button = self.find_element_by_css_selector(
            'a[title="Go to the next page"] > span'
        )
        if next_page_button.is_enabled():
            next_page_button.click()
            time.sleep(3)
        else:
            self.close()


class FormulaDictionary:
    def __init__(self, executable_path, config_path):
        self.scraper = Scraper(executable_path, config_path)
        self.dic_list = []

    def proc(self):
        self.scraper.login()
        self.scraper.to_formulas_page()
        while True:
            try:
                self.formulas_from_page(self.scraper.page_source)
                self.scraper.to_next_page_or_finish()
            except:
                break

    def formula_from_tr(self, tr) -> dict:
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
        print(self.dic_list[-1])

    def extract_formula(self, table) -> list:
        for tr in table.find_all("tr")[1:]:
            self.formula_from_tr(tr)

    def formulas_from_page(self, page_source) -> list:
        self.extract_formula(BeautifulSoup(page_source, "html.parser").find_all("table")[-1])


if __name__ == "__main__":
    formulas = FormulaDictionary("../chromedriver.exe", "okchundang.ini")
    formulas.proc()
    with open("ok_formulas.pickle", "wb") as file:
        pickle.dump(formulas.dic_list, file)
