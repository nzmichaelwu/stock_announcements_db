# import libraries
from webcrawler import afr_scraper
import pandas as pd
from datetime import date, datetime
import sys, os
import subprocess
import yaml
from src.util import DotDict

from sqlalchemy import create_engine

cfg = DotDict(yaml.safe_load(open('/opt/db/config_db.yml')))
# cfg = DotDict(yaml.safe_load(open('config_db.yml')))

# variables
today = date.today().strftime('%Y-%m-%d')
today_s = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Get required database params
DATABASE_URL = 'postgresql://' + cfg.db.user + ":" + cfg.db.password + "@" + cfg.db.host + ":" + str(cfg.db.port) + "/" + cfg.db.name

# get afr data
df_afr_homepage, df_afr_street_talk = afr_scraper(cfg.urls.afr_homepage, cfg.urls.afr_street_talk, today_s)
print(f"{df_afr_homepage.shape} of records have been scraped from afr homepage...")
print(f"{df_afr_street_talk.shape} of records have been scraped from afr street talk...")

### Save data to AWS Postgresql DB ----
postgresql_engine = create_engine(DATABASE_URL)

df_afr_homepage.to_sql('afr_homepage', con=postgresql_engine, if_exists='append')
df_afr_street_talk.to_sql('afr_street_talk', con=postgresql_engine, if_exists='append')

postgresql_engine.dispose() # dispose engine

# check whether the table load is successful
num_rows_afr_homepage = postgresql_engine.execute("Select count(*) from afr_homepage").fetchall()[0][0]
print(f'the afr_homepage table now contains {num_rows_afr_homepage} rows of data...')

num_rows_afr_street_talk = postgresql_engine.execute("Select count(*) from afr_street_talk").fetchall()[0][0]
print(f'the afr_street_talk table now contains {num_rows_afr_street_talk} rows of data...')
# print(postgresql_engine.execute("Select count(*) from announcements").fetchall()
# postgresql_engine.execute("Select pg_size_pretty(pg_total_relation_size('announcements'))").fetchall()  # check table size
