# import libraries
import time

import pandas as pd
import regex as re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


### function to scrape hotcopper website ----
def hotcopper_scraper(base_url, run_date):
    response_hc = requests.get(base_url, headers={"User-Agent": "Mozilla/5.0"}).content

    html_hc = BeautifulSoup(response_hc, "lxml")

    announcements_table = html_hc.find_all(class_="table is-fullwidth is-hidden-touch")

    stock_pill_td_list = announcements_table[0].findAll(
        "td", {"class": "stock-pill-td"}
    )
    stock_td_list = announcements_table[0].findAll("td", {"class": "stock-td"})
    stock_ps_td_list = announcements_table[0].findAll(
        "td", {"class": "price-sensitive-td"}
    )
    stock_ts_td_list = announcements_table[0].findAll("td", {"class": "stats-td"})

    # extract ticker code
    ticker_code_list = []
    for i in range(0, len(stock_pill_td_list)):
        tag_str = stock_pill_td_list[i].find("a", class_="tag-type-symbol").prettify()
        ticker_code = re.search("\n [a-zA-z\d]{3}", tag_str).group(0).replace("\n ", "")
        ticker_code_list.append(ticker_code)

    # extract announcement
    announcement_list = []
    for i in range(0, len(stock_td_list)):
        tag_str = stock_td_list[i].find("a").prettify()
        announcement = (
            re.search("  [$.\da-z A-Z.,'/&:-]{1,50}", tag_str).group(0).strip()
        )
        announcement_list.append(announcement)

    # extract price sensitive
    price_sensitive_list = []
    for i in range(0, len(stock_ps_td_list)):
        tag_str = stock_ps_td_list[i].prettify()
        if re.search("  [a-z A-Z]{3,20}", tag_str) is None:
            price_sensitive = "NOT PRICE SENSITIVE"
        else:
            price_sensitive = re.search("  [a-z A-Z]{3,20}", tag_str).group(0).strip()
        price_sensitive_list.append(price_sensitive)

    # extract announcement time
    announcement_time_list = []
    for i in range(0, len(stock_ts_td_list), 2):
        tag_str = stock_ts_td_list[i].prettify()
        time = re.search("  [\d]{2}[^a-zA-Z][\d]{2}", tag_str).group(0).strip()
        date_time = run_date + " " + time
        announcement_time_list.append(date_time)

    d_hc = {
        "ticker": ticker_code_list,
        "announcement": announcement_list,
        "price_sensitive": price_sensitive_list,
        "date_time": announcement_time_list,
    }
    df_hc = pd.DataFrame(d_hc)

    return df_hc


### function to scrape market index website ----
def marketindex_scraper(base_url, run_ts):

    # Setup chrome options
    firefox_options = Options()
    firefox_options.headless = True

    # Set path to chromedriver
    webdriver_service = Service("/usr/local/bin/geckodriver")
    driver = webdriver.Firefox(service=webdriver_service, options=firefox_options)

    driver.get(base_url)
    time.sleep(1)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)

    webpage = driver.page_source
    time.sleep(4)

    # start scraping the market index table
    htmlpage = BeautifulSoup(webpage, "lxml")
    table = htmlpage.find("table", class_="mi-table mt-6")
    rows = table.find_all("tr")

    market_cap_data = []

    for i in range(1, len(rows)):
        try:
            row_dict = {}
            values = rows[i].find_all("td")
            if len(values) == 11:
                row_dict["ticker"] = values[2].text
                row_dict["name"] = values[3].find("span").text
                row_dict["price"] = float(values[4].text.replace("$", ""))
                row_dict["market_cap"] = values[10].text
                row_dict["extract_timestamp"] = run_ts
            market_cap_data.append(row_dict)
        except:
            print("Row number: " + str(i))
        finally:
            i = i + 1

    driver.quit()
    df_market_cap = pd.DataFrame(market_cap_data)

    return df_market_cap


### function to scrape AFR website (front page headline and street talk section) ----
def afr_scraper(homepage_url, street_talk_url, run_ts):
    # extract homepage headlines
    response_afr = requests.get(
        homepage_url, headers={"User-Agent": "Mozilla/5.0"}
    ).content
    html_afr = BeautifulSoup(response_afr, "lxml")

    main_contents = html_afr.find_all("h3")

    headlines = []

    for content in main_contents:
        headlines.append(content.text.strip())

    d_headlines = {"headline": headlines, "extract_ts": run_ts}
    df_afr_headlines = pd.DataFrame(d_headlines)

    # extract street talk headlines
    response_street_talk = requests.get(
        street_talk_url, headers={"User-Agent": "Mozilla/5.0"}
    ).content
    html_street_talk = BeautifulSoup(response_street_talk, "lxml")

    street_talk_table = html_street_talk.find_all(class_="_3lKkv")
    street_talk_list = street_talk_table[0].findAll("div", {"class": "_2slqK _3AC43"})

    street_talk_headlines_list = []
    street_talk_summary_list = []
    for i in range(0, len(street_talk_list)):
        # headlines
        tag_str_headline = street_talk_list[i].find("a", class_="_235GT")
        street_talk_headline = tag_str_headline.text
        street_talk_headlines_list.append(street_talk_headline)
        # summary
        tag_str_summary = street_talk_list[i].find("p", class_="wI-Bh")
        street_talk_summary = tag_str_summary.text.replace("\xa0", "")
        street_talk_summary_list.append(street_talk_summary)

    d_street_talk = {
        "headline": street_talk_headlines_list,
        "summary": street_talk_summary_list,
        "extract_ts": run_ts,
    }
    df_afr_street_talk = pd.DataFrame(d_street_talk)

    return df_afr_headlines, df_afr_street_talk


"""
  Function to scrape DataRoom and Trading Day, as their format is the same
"""


def australian_section_scrapper(url, run_ts):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).content
    html = BeautifulSoup(response, "lxml")

    main_content = html.find("div", {"id": "group_3_col-471"})
    story_blocks = main_content.find_all(class_="story-block")

    story_category_list = []
    story_heading_list = []
    story_summary_list = []

    for i in range(0, len(story_blocks)):
        story_category = (
            story_blocks[i]
            .find_all(class_="story-block__category")[0]
            .text.replace(" ", "")
        )
        story_category_list.append(story_category)

        story_heading = story_blocks[i].find_all(class_="story-block__heading")[0].text
        story_heading_list.append(story_heading)

        story_summary = (
            story_blocks[i].find_all(class_="story-block__standfirst")[0].text
        )
        story_summary_list.append(story_summary)

    d_dict = {
        "category": story_category_list,
        "heading": story_heading_list,
        "summary": story_summary_list,
        "extract_ts": run_ts,
    }
    df = pd.DataFrame(d_dict).drop_duplicates()

    return df


### function to scrape The Australian website (homepage, dataroom, and trading day section) ----
def aus_scraper(homepage_url, dataroom_url, trading_day_url, run_ts):
    # extract homepage headlines
    response_hp = requests.get(
        homepage_url, headers={"User-Agent": "Mozilla/5.0"}
    ).content
    html_hp = BeautifulSoup(response_hp, "lxml")

    story_blocks_hp = html_hp.find_all(class_="story-block")

    story_category_hp_list = []
    story_heading_hp_list = []

    for i in range(0, len(story_blocks_hp)):
        try:
            story_category_hp = (
                story_blocks_hp[i]
                .find_all(class_="story-block__kicker")[0]
                .text.replace(" ", "")
            )
        except:
            story_category_hp = ""
        story_category_hp_list.append(story_category_hp)

        try:
            story_heading_hp = (
                story_blocks_hp[i]
                .findAll("h3", {"class": "story-block__heading"})[0]
                .text
            )
        except:
            story_heading_hp = ""
        story_heading_hp_list.append(story_heading_hp)

    d_aus_homepage = {
        "category": story_category_hp_list,
        "heading": story_heading_hp_list,
        "extract_ts": run_ts,
    }

    df_aus_homepage = pd.DataFrame(d_aus_homepage).drop_duplicates()
    df_aus_dataroom = australian_section_scrapper(dataroom_url, run_ts)
    df_aus_tradingday = australian_section_scrapper(trading_day_url, run_ts)

    return df_aus_homepage, df_aus_dataroom, df_aus_tradingday
