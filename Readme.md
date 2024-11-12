This is a massive scraper that scrapes all rewards/offers from Rakuten and can either log results to the console, a JSON file, a database, or the log handler for the app, or any combination of these.

NOTE: This must use Python v3.12, anything later will produce unexpected results.

# Installation
1) py -v3.12 -m venv scraper
2) cd scraper
3) Scripts/activate.bat (or on linux, source bin/activate)
4) copy app/example.env app/.env
5) configure .env file
6) pip install -r app/requirements.txt