import pickle
import time

from bs4 import BeautifulSoup
from selenium import webdriver

from config import *

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
try:
    driver = webdriver.Chrome('chromedriver.exe', options=options)
except:
    driver = webdriver.Chrome('chromedriver', options=options)

driver.get(ok_login_url)
driver.find_element_by_id(ok_id_input).send_keys(ok_id)
driver.find_element_by_id(ok_pwd_input).send_keys(ok_pwd)
driver.find_element_by_id(login_button).click()

time.sleep(10)
driver.switch_to.default_content()
driver.get(ok_dict_url)
time.sleep(10)

def extract_data(table):
    data = []
    tr_list = table.find_all('tr')[1:]
    for tr in tr_list:
        try:
            # time.sleep(1)
            div_list = tr.find_all('div')
            formula_type = div_list[1].text
            formula_reference = div_list[2].text
            formula_name = div_list[4].text.split('\xa0')[0]
            span_list = div_list[4].find('div').find_all('span', {'class': 'herb'})
            formula_recipe = {}
            for span in span_list:
                herb_name = span.find_all('span')[0].text
                herb_amount = span.find_all('span')[-1].text
                if len(span.find_all('span')) > 2:
                    cookery = span.find_all('span')[1].text
                else:
                    cookery = ''
                formula_recipe[herb_name] = {'cookery': cookery, 'herb_amount': herb_amount}
            herbs_count = int(div_list[6].text)
            assert herbs_count == len(formula_recipe)
            chub =div_list[7].text.replace('\xa0', '')
            formula = {
                formula_name:
                     {'formula_type': formula_type, 'formula_reference': formula_reference,
                      'formula_recipe': formula_recipe,
                      'herbs_count': herbs_count,
                      'chub': chub
                      }
                 }
            data.append(formula)
        except:
            print(tr.text)

    return data

whole_data = []

while True:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find_all('table')[-1]
    data = extract_data(table)
    whole_data += data
    next_page_button = driver.find_element_by_css_selector(
        'a[title="Go to the next page"] > span'
    )
    try:
        next_page_button.click()
    except:
        break
    time.sleep(3)

driver.close()

with open('ok_data.pickle', 'wb') as file:
    pickle.dump(whole_data, file)