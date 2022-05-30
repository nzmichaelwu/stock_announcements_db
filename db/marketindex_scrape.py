# import libraries
from webcrawler import marketindex_scraper
import pandas as pd
from datetime import date, datetime
import sys
import subprocess
import yaml
from src.util import DotDict

from sqlalchemy import create_engine

cfg = DotDict(yaml.safe_load(open('config.yml')))

# variables
today = date.today().strftime('%Y-%m-%d')
today_s = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# get market index data
df_mi = marketindex_scraper(cfg.urls.marketindex, today_s)

### Save data to Heroku Postgresql DB ----
postgresql_engine = create_engine(cfg.db.url, echo=False)

df_mi.to_sql('market_index', con=postgresql_engine, if_exists='append') # overwrite instead of append, coz dont need to keep history

# print(postgresql_engine.execute("Select * from market_index").fetchone())