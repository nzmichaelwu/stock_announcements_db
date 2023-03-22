import yaml
from sqlalchemy import create_engine
from src.util import DotDict

cfg = DotDict(yaml.safe_load(open("/opt/db/config_db.yml")))
# cfg = DotDict(yaml.safe_load(open('config_db.yml')))

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

# Connect to database
postgresql_engine = create_engine(DATABASE_URL)


# Truncate announcement table
postgresql_engine.execute("Truncate table announcements")

if (
    postgresql_engine.execute("Select count(*) from announcements").fetchall()[0][0]
    == 0
):
    print("table announcement has been truncated successfully...")
else:
    print("table announcement has been truncated unsuccessfully!")


# Truncate market_index table
postgresql_engine.execute("Truncate Table market_index")

if postgresql_engine.execute("Select count(*) from market_index").fetchall()[0][0] == 0:
    print("table market_index has been truncated successfully...")
else:
    print("table market_index has been truncated unsuccessfully!")


# Truncate afr tables
postgresql_engine.execute("Truncate Table afr_homepage")

if postgresql_engine.execute("Select count(*) from afr_homepage").fetchall()[0][0] == 0:
    print("table afr_homepage has been truncated successfully...")
else:
    print("table afr_homepage has been truncated unsuccessfully!")

postgresql_engine.execute("Truncate Table afr_street_talk")

if (
    postgresql_engine.execute("Select count(*) from afr_street_talk").fetchall()[0][0]
    == 0
):
    print("table afr_street_talk has been truncated successfully...")
else:
    print("table afr_street_talk has been truncated unsuccessfully!")


# Truncate the australian tables
postgresql_engine.execute("Truncate Table aus_homepage")

if postgresql_engine.execute("Select count(*) from aus_homepage").fetchall()[0][0] == 0:
    print("table aus_homepage has been truncated successfully...")
else:
    print("table aus_homepage has been truncated unsuccessfully!")

postgresql_engine.execute("Truncate Table aus_dataroom")

if postgresql_engine.execute("Select count(*) from aus_dataroom").fetchall()[0][0] == 0:
    print("table aus_dataroom has been truncated successfully...")
else:
    print("table aus_dataroom has been truncated unsuccessfully!")

postgresql_engine.execute("Truncate Table aus_tradingday")

if (
    postgresql_engine.execute("Select count(*) from aus_tradingday").fetchall()[0][0]
    == 0
):
    print("table aus_tradingday has been truncated successfully...")
else:
    print("table aus_tradingday has been truncated unsuccessfully!")


# dispose engine
postgresql_engine.dispose()
