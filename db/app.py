# import libraries
import os
import subprocess
import sys
from datetime import date, datetime

import pandas as pd
import yaml
from flask import Flask
from sqlalchemy import create_engine
from src.util import DotDict

# cfg = DotDict(yaml.safe_load(open('/opt/db/config_db.yml')))
cfg = DotDict(yaml.safe_load(open("config_db.yml")))

#### Set up Postgresql Engine ####
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
postgresql_engine = create_engine(DATABASE_URL)

num_rows_hc = postgresql_engine.execute(
    "Select count(*) from announcements"
).fetchall()[0][0]
num_rows_mi = postgresql_engine.execute("Select count(*) from market_index").fetchall()[
    0
][0]
num_rows_afr_homepage = postgresql_engine.execute(
    "Select count(*) from afr_homepage"
).fetchall()[0][0]
num_rows_aus_homepage = postgresql_engine.execute(
    "Select count(*) from aus_homepage"
).fetchall()[0][0]

#### Flask App ####

app = Flask(__name__)


@app.route("/")
def index():
    if (
        (num_rows_hc == 0)
        | (num_rows_mi == 0)
        | (num_rows_afr_homepage == 0)
        | (num_rows_aus_homepage == 0)
    ):
        msg = f"Scraping was UNSUCCESSFUL! Number of rows in announcements table is {num_rows_hc},\n \
        and number of rows in market_index table is {num_rows_mi},\n \
        and number of rows in afr_homepage table is {num_rows_afr_homepage},\n \
        and number of rows in aus_homepage table is {num_rows_aus_homepage}."
    else:
        msg = f"Scraping was SUCCESSFUL! Number of rows in announcements table is {num_rows_hc},\n \
        and number of rows in market_index table is {num_rows_mi},\n \
        and number of rows in afr_homepage table is {num_rows_afr_homepage},\n \
        and number of rows in aus_homepage table is {num_rows_aus_homepage}."

    return msg


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
