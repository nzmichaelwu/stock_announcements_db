# import libraries
from matplotlib.pyplot import hot
from webcrawler import hotcopper_scraper, marketindex_scraper
import pandas as pd
from datetime import date, datetime
import sys
import subprocess
import yaml

import sqlite3 as sql

sys.path.append('..')
from helper_funcs.helper_funcs import util as hf

# pandas display options
pd.options.display.max_columns = None
pd.options.display.max_rows = 350
pd.options.display.max_colwidth = 0

cfg = hf.DotDict(yaml.safe_load(open('config.yml')))

pyfile = hf.fileloc(globals())
logger = hf.setup_logging(__name__, f'{cfg.out.LOGS}/{pyfile}.txt', add_ts=True); logger.l = lambda ls: logger.lbase(ls, globals())
logname = logger.handlers[1].baseFilename.split('/')[-1].split('.')[0]

gitstat = subprocess.run(['git', 'rev-parse', '--verify', 'HEAD'], capture_output=True)
git_commit_short_sha = gitstat.stdout[:7].decode('utf-8')
logger.l('git_commit_short_sha')
logger.info(f"Git Branch:\n{subprocess.check_output(['git', 'branch']).decode('utf8')}")


# variables
today = date.today().strftime('%Y-%m-%d')
today_s = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


### Get relevant data ----
# get hotcopper news headlines
df_hc_news = hotcopper_scraper(cfg.urls.hotcopper, today)
logger.info(f'the shape of df_hc_news is {df_hc_news.shape}.')

# get market index data
df_mi = marketindex_scraper(cfg.urls.marketindex, today_s)
logger.info(f'the shape of df_mi is {df_mi.shape}.')

# create a combined dataframe
df_stock = (
  df_mi.merge(df_hc_news, how='left', on='ticker') \
    .sort_values('ticker') \
      .reset_index(drop=True)
)
logger.info(f'the shape of df_stock is {df_stock.shape}.')


### Save data to SQL DB ----
conn = sql.connect('stock.db')
df_stock.to_sql('announcements', conn, if_exists='append')