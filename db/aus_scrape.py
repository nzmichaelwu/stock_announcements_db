# import libraries
import os
import subprocess
import sys
from datetime import date, datetime

import pandas as pd
import yaml
from sqlalchemy import create_engine
from src.util import DotDict
from webcrawler import aus_scraper

cfg = DotDict(yaml.safe_load(open("/opt/db/config_db.yml")))
# cfg = DotDict(yaml.safe_load(open('config_db.yml')))

# variables
today = date.today().strftime("%Y-%m-%d")
today_s = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Get required database params
DATABASE_URL = (
    "postgresql://"
    + cfg.db.user
    + ":"
    + cfg.db.password
    + "@"
    + cfg.db.host
    + ":"
    + str(cfg.db.port)
    + "/"
    + cfg.db.name
)

# get the australian data
df_aus_homepage, df_aus_tradingday = aus_scraper(
    cfg.urls.aus_homepage, cfg.urls.aus_tradingday, today_s
)
print(
    f"{df_aus_homepage.shape} of records have been scraped from The Australian homepage..."
)
# print(
#     f"{df_aus_dataroom.shape} of records have been scraped from The Australian Data Room..."
# )
print(
    f"{df_aus_tradingday.shape} of records have been scraped from The Australian Trading Day..."
)

### Save data to AWS Postgresql DB ----
postgresql_engine = create_engine(DATABASE_URL)

df_aus_homepage.to_sql("aus_homepage", con=postgresql_engine, if_exists="append")
# df_aus_dataroom.to_sql("aus_dataroom", con=postgresql_engine, if_exists="append")
df_aus_tradingday.to_sql("aus_tradingday", con=postgresql_engine, if_exists="append")

postgresql_engine.dispose()  # dispose engine

# check whether the table load is successful
num_rows_aus_homepage = postgresql_engine.execute(
    "Select count(*) from aus_homepage"
).fetchall()[0][0]
print(f"the aus_homepage table now contains {num_rows_aus_homepage} rows of data...")

# num_rows_aus_dataroom = postgresql_engine.execute(
#     "Select count(*) from aus_dataroom"
# ).fetchall()[0][0]
# print(f"the aus_dataroom table now contains {num_rows_aus_dataroom} rows of data...")

num_rows_aus_tradingday = postgresql_engine.execute(
    "Select count(*) from aus_tradingday"
).fetchall()[0][0]
print(
    f"the aus_tradingday table now contains {num_rows_aus_tradingday} rows of data..."
)
# print(postgresql_engine.execute("Select count(*) from announcements").fetchall()
# postgresql_engine.execute("Select pg_size_pretty(pg_total_relation_size('announcements'))").fetchall()  # check table size
