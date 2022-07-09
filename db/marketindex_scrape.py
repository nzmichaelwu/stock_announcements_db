# import libraries
from webcrawler import marketindex_scraper
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

# get market index data
df_mi = marketindex_scraper(cfg.urls.marketindex, today_s)
print(f"{df_mi.shape} of records have been scraped from market_index...")

### Save data to AWS Postgresql DB ----
postgresql_engine = create_engine(DATABASE_URL)

df_mi.to_sql('market_index', con=postgresql_engine, if_exists='replace') # overwrite instead of append, coz dont need to keep history

postgresql_engine.dispose() # dispose engine

# check whether the table load is successful
num_rows_mi = postgresql_engine.execute("Select count(*) from market_index").fetchall()[0][0]
print(f'the market_index table now contains {num_rows_mi} rows of records...')
# print(postgresql_engine.execute("Select count(*) from market_index").fetchall())
