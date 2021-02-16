from selenium import webdriver
from config import *

driver = webdriver.Chrome('../chromedriver.exe')
driver.get('naver.com')
driver.close()