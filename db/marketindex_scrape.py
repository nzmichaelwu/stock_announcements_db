# import libraries
from webcrawler import marketindex_scraper
import pandas as pd
from datetime import date, datetime
import sys, os
import subprocess
import yaml
from src.util import DotDict

from sqlalchemy import create_engine

cfg = DotDict(yaml.safe_load(open('db/config_db.yml')))

# variables
today = date.today().strftime('%Y-%m-%d')
today_s = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# read database connection url from the enivron variable we just set.
DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASE_URL_mod = DATABASE_URL.replace("postgres", "postgresql") # refer to https://stackoverflow.com/questions/62688256/sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy-dialectspostgre

# get market index data
df_mi = marketindex_scraper(cfg.urls.marketindex, today_s)

### Save data to Heroku Postgresql DB ----
postgresql_engine = create_engine(DATABASE_URL, echo=False)

df_mi.to_sql('market_index', con=postgresql_engine, if_exists='replace') # overwrite instead of append, coz dont need to keep history

postgresql_engine.dispose() # dispose engine

# print(postgresql_engine.execute("Select * from market_index").fetchone())