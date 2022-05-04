# import libraries
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import regex as re
from datetime import date

# variables
url_hc = 'https://hotcopper.com.au/announcements/asx/'
url_mi = 'https://www.marketindex.com.au/asx-listed-companies'
today = date.today().strftime('%Y-%m-%d')

req = Request(url=url_hc, headers={'user-agent': 'my-scraper/0.1'})
response = urlopen(req)

html = BeautifulSoup(response, 'lxml')

announcements_table = html.find_all(class_ = "table is-fullwidth is-hidden-touch")

stock_pill_td_list = announcements_table[0].findAll('td', {'class': 'stock-pill-td'})
stock_td_list = announcements_table[0].findAll('td', {'class': 'stock-td'})
stock_ps_td_list = announcements_table[0].findAll('td', {'class': 'price-sensitive-td'})
stock_ts_td_list = announcements_table[0].findAll('td', {'class': 'stats-td'})

# extract ticker code
ticker_code_list = []
for i in range(0, len(stock_pill_td_list)):
  tag_str = stock_pill_td_list[i].find('a', class_ = 'tag-type-symbol').prettify()
  ticker_code = re.search('\n [a-zA-z\d]{3}', tag_str).group(0).replace('\n ','')
  ticker_code_list.append(ticker_code)

# extract announcement
announcement_list = []
for i in range(0, len(stock_td_list)):
  tag_str = stock_td_list[i].find('a').prettify()
  announcement = re.search('  [\da-z A-Z]{1,50}', tag_str).group(0).strip()
  announcement_list.append(announcement)

# extract price sensitive
price_sensitive_list = []
for i in range(0, len(stock_ps_td_list)):
  tag_str = stock_ps_td_list[i].prettify()
  if re.search('  [a-z A-Z]{3,20}', tag_str) is None:
    price_sensitive = 'NOT PRICE SENSITIVE'
  else:
    price_sensitive = re.search('  [a-z A-Z]{3,20}', tag_str).group(0).strip()
  price_sensitive_list.append(price_sensitive)

# extract announcement time
announcement_time_list = []
for i in range(0, len(stock_ts_td_list), 2):
  tag_str = stock_ts_td_list[i].prettify()
  time = re.search('  [\d]{2}[^a-zA-Z][\d]{2}', tag_str).group(0).strip()
  date_time = today + ' ' + time
  announcement_time_list.append(date_time)

d_hc = {'ticker': ticker_code_list, 'announcement': announcement_list, 'price_sensitive': price_sensitive_list, 'date_time': announcement_time_list}
df_hc = pd.DataFrame(d_hc)