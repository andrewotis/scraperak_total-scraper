import time

async def scroll_to_bottom(page, url, config):
    dom_height = await page.evaluate('''(() => window.innerHeight + window.scrollY)();''')
    prev_dom_height = None
    height_unchanged_counter = 0
    while True:
      time.sleep(config.sleep_before_scroll)
      await page.evaluate('''!async function(){let n=await document.evaluate("//*[contains(@class, 'chakra-link') and contains(@class, 'css-187ams7')]",document,null,XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,null),a=n.snapshotLength-1;n.snapshotItem(a).scrollIntoView()}();''')
      for x in range(1,25):
        await page.keyboard.press("ArrowDown")
      if prev_dom_height is None:
        prev_dom_height = dom_height
      elif prev_dom_height == dom_height:
        if height_unchanged_counter == 2:
          break
        else:
          height_unchanged_counter += 1
      else:
        prev_dom_height = dom_height
      dom_height = await page.evaluate('''(() => window.innerHeight + window.scrollY)();''')