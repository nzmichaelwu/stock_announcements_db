import yaml
from src.util import DotDict

from sqlalchemy import create_engine

cfg = DotDict(yaml.safe_load(open('/opt/db/config_db.yml')))
# cfg = DotDict(yaml.safe_load(open('config_db.yml')))

# Get required database params
DATABASE_URL = 'postgresql://' + cfg.db.user + ":" + cfg.db.password + "@" + cfg.db.host + ":" + str(cfg.db.port) + "/" + cfg.db.name

# Connect to database
postgresql_engine = create_engine(DATABASE_URL)

# Truncate announcement table
postgresql_engine.execute("Truncate table announcements")

if postgresql_engine.execute("Select count(*) from announcements").fetchall()[0][0] == 0:
  print("table announcement has been truncated successfully...")
else:
  print("table announcement has been truncated unsuccessfully!")

# Truncate market_index table
postgresql_engine.execute("Truncate Table market_index")

if postgresql_engine.execute("Select count(*) from market_index").fetchall()[0][0] == 0:
  print("table market_index has been truncated successfully...")
else:
  print("table market_index has been truncated unsuccessfully!")


# dispose engine
postgresql_engine.dispose()