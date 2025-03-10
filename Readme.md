This is a massive scraper that scrapes all rewards/offers from Rakuten and can either log results to the console, a JSON file, a database, or the log handler for the app, or any combination of these.

# NOTES:
- This must use Python v3.12, anything later will produce unexpected results. Check the pyvenv.cfg file.
- Building this was a lot of trial and error. Over time, I whittled down reliance in Playwright to what is now only scrolling the infinite-scroll, taking screenshots, and getting the page source. From there, I load the source and use lxml and XPath queries to traverse the DOM and extract the data
- Rakuten lists the same store/offer in multiple categories. So each entry is included with what category it came from in case categories are needed
- Infinite-scrolling: Rakuten category pages use infinite-scrolling to load data real time as you scroll down the screen. This prevents a challenge for ensuring every possible offer is visible on the page to collect. The solution I came up with was to inject a custom javascript script into the page using Playwright that finds the very last offer on the screen and scrolls to it, waits for the page to load, and repeats while tracking page height across all scrolling. Once there are several scroll attempts without changes in the page height, it is safe to assume all offers are visible.

# Features
- screenshots
- sms alerting if something goes wrong
- sms reporting
- extensively configurable. every detail from timeouts to whether or not to use concurrent futures to enabling screenshots is configurable
- queueing and retries: the scraper will keep trying until it gathers all rewards on all categories
- easy category maintenance: the pages to scrape are listed in a plain txt file (app/config.txt) and this can be modified easily to include new categories or remove unwanted ones[
- when the scraper retrieves an offer/reward, there is a watcher (Observer patern) that can trigger logging the reward to the console, a JSON file, a database, or the app's log handlers. this way, any number of combinations can be used for the rewards output
- route interceptor: since we are loading quite a bit of pages/data, there is a route interceptor feature that will block certain web requests like fonts, 3rd party javascript files, google analytics, and more. this substantially cuts down on page loading time
- dynamic sleeping: sometimes certain parts of the scrape require a sleep and sometimes they dont depending on how many rewards are available. rather than configure a value for this, the scrape is first tried without sleeps. if it ends up needing to use them, it will incrementally add one second to each sleep setting each time it does a pass

# Database
- Uses SQLAlchemy Models and relationships
- There's a package named dbmodule that can be pip installed into any of the needed folders locally (scraper, api, etc)
- Includes seeders for offer types and reward types that also generate the schema
- Includes models with relationships for all DB tables needed to store results
- Everything is split out into separate tables. For example, reward_type and offer_type are just an id referenced from the rewards table. This has helped speed things up drastically

# Screenshots
- Are entire page screenshots and can be VERY big both visually and with regard to file-size
- Are able to be configured to be stored locally in a specified path or to be stored on AWS S3
- Are PNG and of sufficient quality to zoom in and read offers
- The screenshots will save in the following format meaning there is a maximum of one screenshot per category page per hour.

# Logging

# Installation
1) py -v3.12 -m venv scraper
2) cd scraper
3) Scripts/activate.bat (or on linux, source bin/activate)
4) copy app/example.env app/.env
5) configure .env file
6) pip install -r app/requirements.txt