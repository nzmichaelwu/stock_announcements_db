# import libraries
from webcrawler import hotcopper_scraper
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

# get hotcopper news headlines
df_hc_news = hotcopper_scraper(cfg.urls.hotcopper, today)

### Save data to Heroku Postgresql DB ----
postgresql_engine = create_engine(cfg.db.url, echo=False)

df_hc_news.to_sql('announcements', con=postgresql_engine, if_exists='append')

# print(postgresql_engine.execute("Select * from announcements").fetchone())