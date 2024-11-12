import asyncio
import time
from rich import print
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor
from playwright.async_api import async_playwright
from yarl import URL
from lib.screenshot import take_screenshot
from lib.intercept import intercept_route
from lib.Counter import Counter
from lib.popups import close_popup
from lib.send_sms import send_sms_report
from lib.init_loggers import logify
from lib.scroller import scroll_to_bottom
from lib.Timer import Timer
from lib.Config import Config
from lib.source import gather_offers
from lib.Queue import Queue
import traceback

def get_category_from_url(url):
    return url.path.replace("/", "").replace("-", "_")

async def get_page_source(page, url):
    category = get_category_from_url(url)
    logger.info(f"Gathering source from page: {url}")
    html_content = await page.content()
    if html_content != "":
        logger.info(f"Page source retrieved")
        source.append({
            'category': category,
            'source': html_content
        })

async def scrape_page(page, path):
    url = URL(path)
    category = get_category_from_url(url)
    logger.info(f"Loading page: {url}")
    retries = 0
    while retries < config.max_retries:
        try:
            if config.use_route_intercept is True:
                await page.route("**/*", intercept_route)

            await page.goto(url.human_repr(), wait_until='domcontentloaded', timeout=config.timeout)
            await close_popup(page, url, logger, config)
            await scroll_to_bottom(page, url, config)
            time.sleep(config.sleep_after_scroll)

            if config.take_screenshots is True:
                await take_screenshot(page, url.path, logger, config)

            time.sleep(config.sleep_after_screenshot)
            await get_page_source(page, url)
            queue.remove
            return
        except Exception as e:
            logger.error(f"Error scraping {path}: {e}")
            print("[bold red]" + traceback.format_exc() + "[/bold red]")
            retries += 1
            logger.error(f"Failed to scrape {path} after {config.max_retries} retries")
            counter.increment(category, 'scrape_failures')
            if retries < config.max_retries:
                time.sleep(config.sleep_between_retries)
            else:
                queue.add(path)

async def worker(path):
    async with async_playwright() as p:
        browser = await p.chromium.connect(f"ws://localhost:3000/chromium/playwright?token={config.browserless_io_token}")
        # browser = await p.chromium.launch(headless=os.getenv("USE_HEADLESS") == "True")
        context = await browser.new_context()
        try:
            page = await context.new_page()
            result = await scrape_page(page, path)
            return result
        finally:
            await browser.close()

async def main():
    console = Console()
    console.clear()
    print("Starting ScrapeRak: the best Rakuten scraper. ever.")
    timer = Timer()
    if config.max_workers == 1:
        for path in config.urls:
            await worker(path)
    else:
        running = True
        while running:
            urls = queue.all()
            loop = asyncio.get_running_loop()
            with ThreadPoolExecutor(max_workers=config.max_workers) as pool:
                tasks = [
                    loop.run_in_executor(pool, lambda p=path: asyncio.run(worker(p)))
                    for path in urls
                ]
            if queue.is_empty():
                running = False

    offers = await gather_offers(source, config, logger)
    report = counter.report()
    run_time = timer.stop()

    send_sms_report(run_time, report, [], counter, logger)
    logger.info("Rakuten scrape finished in " + str(run_time))

if __name__ == "__main__":
    source = []
    config = Config()
    queue = Queue(config.urls)
    logger = logify(config.logging_level)
    counter = Counter()
    asyncio.run(main())