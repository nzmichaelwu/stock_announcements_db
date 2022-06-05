# import libraries
from webcrawler import hotcopper_scraper
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

# get hotcopper news headlines
df_hc_news = hotcopper_scraper(cfg.urls.hotcopper, today)

### Save data to Heroku Postgresql DB ----
postgresql_engine = create_engine(DATABASE_URL_mod, echo=False)

df_hc_news.to_sql('announcements', con=postgresql_engine, if_exists='append')

postgresql_engine.dispose() # dispose engine

# print(postgresql_engine.execute("Select * from announcements").fetchone())