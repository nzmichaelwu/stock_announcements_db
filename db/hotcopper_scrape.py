# import libraries
import os
import subprocess
import sys
from datetime import date, datetime

import pandas as pd
import yaml
from sqlalchemy import create_engine
from src.util import DotDict
from webcrawler import hotcopper_scraper

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
    + "?sslmode=require"
)

# get hotcopper news headlines
df_hc_news = hotcopper_scraper(cfg.urls.hotcopper, today)
print(f"{df_hc_news.shape} of records have been scraped from hotcopper...")

### Save data to AWS Postgresql DB ----
postgresql_engine = create_engine(DATABASE_URL)

df_hc_news.to_sql("announcements", con=postgresql_engine, if_exists="append")

postgresql_engine.dispose()  # dispose engine

# check whether the table load is successful
num_rows_hc = postgresql_engine.execute(
    "Select count(*) from announcements"
).fetchall()[0][0]
print(f"the announcements table now contains {num_rows_hc} rows of announcements...")
# print(postgresql_engine.execute("Select count(*) from announcements").fetchall()
# postgresql_engine.execute("Select pg_size_pretty(pg_total_relation_size('announcements'))").fetchall()  # check table size
