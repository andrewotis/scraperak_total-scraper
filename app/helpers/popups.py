import time

async def close_popup(page, url, app):
    close_buttons = await page.get_by_label("Close").all()
    if close_buttons is None:
        return
    else:
        for close_button in close_buttons:
            button_class = await close_button.get_attribute("class", timeout=app.get('config').timeout)
            if button_class is not None and "modal__close" in button_class:
                await close_button.click()
                app.get('logger').info(f"Closing popup: {url}")

            await page.wait_for_load_state('domcontentloaded')
            time.sleep(app.get('counter').passes)
    return True