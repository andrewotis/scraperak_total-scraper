import asyncio
import time
from rich import print
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor
from playwright.async_api import async_playwright
from yarl import URL
from helpers.screenshot import take_screenshot
from helpers.intercept import intercept_route
from Classes.Counter import Counter
from helpers.popups import close_popup
from helpers.send_sms import send_sms_report
from helpers.init_loggers import logify
from helpers.scroller import scroll_to_bottom
from Classes.Timer import Timer
from Classes.Config import Config
from helpers.source import gather_offers
from Classes.Queue import Queue
import traceback
from app.database.models.Scrape import Scrape
from tortoise.functions import Max

def get_category_from_url(url):
    return url.path.replace("f/", "").replace("-", "_").replace("/", "")

async def get_page_source(page, url):
    category = get_category_from_url(url)
    html_content = await page.content()
    if html_content != "":
        logger.info(f"Page source retrieved: {url}")
        source.append({
            'category': category,
            'source': html_content
        })

async def scrape_page(page, path):
    url = URL(path)
    category = get_category_from_url(url)
    logger.info(f"Loading page: {url}")

    try:
        if config.use_route_intercept is True:
            await page.route("**/*", intercept_route)

        await page.goto(url.human_repr(), wait_until='domcontentloaded', timeout=config.timeout)
        await close_popup(page, url, logger, config, counter)
        await scroll_to_bottom(page, url, config, counter)
        time.sleep(counter.passes)

        if config.take_screenshots is True:
            await take_screenshot(page, url.path, logger, config)

        time.sleep(counter.passes + 1)
        await get_page_source(page, url)
        queue.remove(path)
        return
    except Exception as e:
        logger.error(f"Error scraping {path}: {e}")
        print("[bold red]" + traceback.format_exc() + "[/bold red]")
        logger.error(f"Failed to scrape {path}. Adding back to the end of the queue to try again later")
        queue.add(path)
        counter.increment(category, 'scrape_retries')

async def worker(path):
    async with async_playwright() as p:
        browser = await p.chromium.connect(config.browserless_connection_string)
        context = await browser.new_context()
        try:
            page = await context.new_page()
            result = await scrape_page(page, path)
            return result
        finally:
            await browser.close()

async def main():
    timer = Timer()
    running = True
    while running:
        if counter.passes > 0:
            logger.info(f"Taking another pass through some categories that didn't scrape properly. There are {queue.size()} items in the queue still.")
        urls = queue.all()
        if config.max_workers == 1:
            for path in urls:
                await worker(path)
        else:
            loop = asyncio.get_running_loop()
            with ThreadPoolExecutor(max_workers=config.max_workers) as pool:
                tasks = [
                    loop.run_in_executor(pool, lambda p=path: asyncio.run(worker(p)))
                    for path in urls
                ]
        if queue.is_empty():
            logger.info("Finished visiting all the pages in the queue.")
            running = False
        counter.increment_passes()
        if counter.passes == config.max_retries:
            logger.error(f"Tried {counter.passes} passes and could not scrape everything.")
            running = False

    await gather_offers(source, config, logger)
    report = counter.report()
    run_time = timer.stop()

    # update the most recent scrape in the database to include the execution_time
    scrape = await Scrape.all().annotate(latest_created_at=Max("created_at")).values("latest_created_at")
    scrape.execution_time = run_time
    scrape.total_workers = config.max_workers
    scrape.total_passes = counter.passes
    scrape.save()

    send_sms_report(run_time, report, [], counter, logger)
    logger.info("Rakuten scrape finished in " + str(run_time))

if __name__ == "__main__":
    console = Console()
    console.clear()
    print("Starting ScrapeRak: the best Rakuten scraper. ever.")
    source = []
    config = Config()
    logger = logify(config.logging_level)
    queue = Queue(config.urls, logger)
    counter = Counter()
    asyncio.run(main())