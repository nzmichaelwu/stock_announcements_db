# import libraries
from ast import excepthandler
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import time
import pandas as pd
import regex as re
from datetime import date, datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# variables
url_hc = 'https://hotcopper.com.au/announcements/asx/'
url_mi = 'https://www.marketindex.com.au/asx-listed-companies'
today = date.today().strftime('%Y-%m-%d')
today_s = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

### scraping hotcopper website ----
req_hc = Request(url=url_hc, headers={'user-agent': 'my-scraper/0.1'})
response_hc = urlopen(req_hc)

html_hc = BeautifulSoup(response_hc, 'lxml')

announcements_table = html_hc.find_all(class_ = "table is-fullwidth is-hidden-touch")

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

# ### scraping market index website ----

'''
  Selenium setup
'''

# Setup chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")

# Set path to chromedriver
webdriver_service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

driver.get(url_mi)
time.sleep(1)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
time.sleep(2)

webpage = driver.page_source
time.sleep(4)

# start scraping the market index table
htmlpage = BeautifulSoup(webpage, 'lxml')
table = htmlpage.find('table', class_='mi-table mt-6')
rows = table.find_all('tr')

market_cap_data = []

for i in range(1, len(rows)):
  try:
    row_dict = {}
    values = rows[i].find_all('td')
    if len(values) == 12:
      row_dict["ticker"] = ticker = values[2].text
      row_dict["name"] = values[3].find('span').text
      row_dict["price"] = float(values[5].text.replace('$',''))
      row_dict["market_cap"] = values[11].text
      row_dict["extract_timestamp"] = today_s
    market_cap_data.append(row_dict)
  except:
    print("Row number: " + str(i))
  finally:
    i = i + 1

driver.quit()
df_market_cap = pd.DataFrame(market_cap_data)