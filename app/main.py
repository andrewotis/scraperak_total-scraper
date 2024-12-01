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
from Classes.Context import Context
import traceback

def get_category_from_url(url):
    return url.path.replace("f/", "").replace("-", "_").replace("/", "")

async def get_page_source(page, url):
    category = get_category_from_url(url)
    html_content = await page.content()
    if html_content != "":
        app.get('logger').info(f"Page source retrieved: {url}")
        source.append({
            'category': category,
            'source': html_content
        })

async def scrape_page(page, path):
    url = URL(path)
    category = get_category_from_url(url)
    app.get('logger').info(f"Loading page: {url}")

    try:
        if app.get('config').use_route_intercept:
            await page.route("**/*", intercept_route)

        await page.goto(url.human_repr(), wait_until='domcontentloaded', timeout=app.get('config').timeout)
        await close_popup(page, url, app)
        await scroll_to_bottom(page, url, app)
        time.sleep(app.get('counter').passes)

        if app.get('config').take_screenshots is True:
            await take_screenshot(page, url.path, app)

        time.sleep(app.get('counter').passes + 1)
        await get_page_source(page, url)
        app.get('queue').remove(path)
        return
    except Exception as e:
        app.get('logger').error(f"Error scraping {path}: {e}")
        print("[bold red]" + traceback.format_exc() + "[/bold red]")
        app.get('logger').error(f"Failed to scrape {path}. Adding back to the end of the queue to try again later")
        app.get('queue').add(path)
        app.get('counter').increment(category, 'scrape_retries')

async def worker(path):
    async with async_playwright() as p:
        browser = await p.chromium.connect(app.get('config').browserless_connection_string)
        context = await browser.new_context()
        try:
            page = await context.new_page()
            result = await scrape_page(page, path)
            return result
        finally:
            await browser.close()

async def main():
    timer = Timer()
    app.add('timer', timer)

    running = True
    while running:
        if app.get('counter').passes > 0:
            app.get('logger').info(f"Taking another pass through some categories that didn't scrape properly. There are {app.get('queue').size()} items in the queue still.")
        urls = app.get('queue').all()
        if app.get('config').max_workers == 1:
            for path in urls:
                await worker(path)
        else:
            loop = asyncio.get_running_loop()
            with ThreadPoolExecutor(max_workers=app.get('config').max_workers) as pool:
                tasks = [
                    loop.run_in_executor(pool, lambda p=path: asyncio.run(worker(p)))
                    for path in urls
                ]
        if app.get('queue').is_empty():
            app.get('logger').info("Finished visiting all the pages in the queue.")
            running = False
        app.get('counter').increment_passes()
        if app.get('counter').passes == app.get('config').max_retries:
            app.get('logger').error(f"Tried {app.get('counter').passes} passes and could not scrape everything.")
            running = False

    await gather_offers(source, app)
    run_time = app.get('timer').stop()

    app.get('watcher').finished()

    send_sms_report(app)
    app.get('logger').info("Rakuten scrape finished in " + str(run_time))

if __name__ == "__main__":
    app = Context()
    console = Console()
    app.add('console', console)
    app.get('console').clear()

    print("[blue]Starting ScrapeRak: the best Rakuten scraper. ever.[/blue]")
    source = []

    config = Config()
    app.add('config', config)

    logger = logify(app.get('config').logging_level)
    app.add('logger', logger)

    queue = Queue(app.get('config').urls, logger)
    app.add('queue', queue)

    counter = Counter()
    app.add('counter', counter)

    asyncio.run(main())
