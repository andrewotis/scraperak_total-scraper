from datetime import datetime

async def take_screenshot(page, path, logger, config):
    date_for_path = datetime.now().strftime('%Y-%m-%d_%H')
    screenshot_path = f"screenshots/{date_for_path}/{path.replace("f/", "").replace("/", "")}.png"
    await page.screenshot(path=screenshot_path, full_page=True, timeout=config.timeout)
    logger.info(f"Screenshot saved: {screenshot_path}")