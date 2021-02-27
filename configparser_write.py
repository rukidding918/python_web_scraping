from selenium import webdriver
from configparser import ConfigParser

config =ConfigParser()
config['personal'] = {
    'id': 'miallsc',
    'password': '2w3e4r5t',
}
config['db'] = {
    'host':'',
    'database': 'lunchDB',
    'user': 'rukidding918@gmail.com',
    'password': '856-Kim-856'
}
config['mysite'] = {
    'url': 'https://aptdeal.shop',
    'port': 3306,
    'python_path': '/usr/local',
    'python_version': '3',
    'python_library': 'flask'
}

config['python_settings'] = {
    'package_path': '${mysite:python_path}/bin/python${mysite:python_version}'
}

with open('dev.ini', 'w') as f:
    config.write(f)
