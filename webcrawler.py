# import libraries
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

# variables
url_hc = 'https://hotcopper.com.au/announcements/asx/'
url_mi = 'https://www.marketindex.com.au/asx-listed-companies'

req = Request(url=url_hc, headers={'user-agent': 'my-scraper/0.1'})
response = urlopen(req)

html = BeautifulSoup(response, 'lxml')

announcements_table = html.find_all(class_ = "table is-fullwidth is-hidden-touch")

announcements_table[0].findAll('tr')