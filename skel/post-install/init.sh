#!/bin/bash

set -e

bash /heroku_login.sh

echo "Executing hotcopper_scrape.py..."
DATABASE_URL=$(heroku config:get DATABASE_URL -a mw-stock-announcement-db) python /opt/db/hotcopper_scrape.py
echo "hotcopper_scrape.py completed..."

sleep 2

echo "Executing marketindex_scrape.py..."
DATABASE_URL=$(heroku config:get DATABASE_URL -a mw-stock-announcement-db) python /opt/db/marketindex_scrape.py
echo "marketindex.py completed..."

echo "Scraping completed."