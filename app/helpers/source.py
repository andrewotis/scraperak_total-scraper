from lxml import html
import traceback
from Observers.ScrapeWatcher import ScrapeWatcher
from Observers.Console import Console
from Observers.MySQL import MySQL
from Observers.Log import Log
from Observers.File import File

async def serialize_element(element):
    return html.tostring(element, pretty_print=True, encoding="unicode")

async def parse_store_url(shopping_link):
    return shopping_link.replace('www.rakuten.com/', '').split("_")[0]

async def process_dollar_reward_amount(offer):
    return float(offer.split(" ")[0].replace("$", ""))

async def process_percentage_reward_amount(offer):
    return float(offer.split("%")[0])

async def parse_offer(offer):
    clean = offer.replace("Up to ", "").replace(" Cash Back", "")
    reward_amount = ""
    reward_type = ""
    try:
        if "%" in clean:
            reward_type = 'percentage'
            reward_amount = await process_percentage_reward_amount(clean)
        elif "$" in clean:
            reward_type = 'dollar'
            reward_amount = await process_dollar_reward_amount(clean)
        else:
            raise Exception(f"Unknown reward type! {offer}")
    except ValueError:
        print(f"String to float issue: {offer}")

    if "Online" in offer or "Cash Back" in offer:
        offer_type = 'online'
    elif "In-Store" in offer:
        offer_type = 'in-store'
    else:
        raise Exception(f"Unknown offer type! {offer}")
    if reward_amount == "" or reward_amount is None:
        raise Exception(f"Unknown Amount! {offer}")
    if reward_type == "" or reward_type is None:
        raise Exception(f"Unknown reward Type! {offer}")
    if offer_type == "" or offer_type is None:
        raise Exception(f"Unknown offer Type! {offer}")
    return reward_type, reward_amount, offer_type

async def process_agroup(agroup_element, category):
    source = await serialize_element(agroup_element)
    agroup_tree = html.fromstring(source)

    link = agroup_tree.xpath("//a/@href")[0]
    store_url = await parse_store_url(link)

    if link == 'https://www.rakuten.com/in-store.htm':
        return None

    try:
        store = agroup_tree.xpath("//span/text()")[0]
        offer = agroup_tree.xpath("//span/text()")[1]
        reward_type, reward_amount, offer_type = await parse_offer(offer)
        return {
            'category' : category,
            'store' : store,
            'reward_type' : reward_type,
            'reward_amount' : reward_amount,
            'offer_type' : offer_type,
            'shopping_url' : link,
            'store_url' : store_url
        }

    except Exception as e:
        print(link)
        print(traceback.format_exc())

async def initialize_observers(config, logger):
    subject = ScrapeWatcher(logger=logger, config=config)

    observers = []
    if config.enable_console_output:
        console = Console()
        observers.append(console)
    if config.enable_database_writing:
        mysql = MySQL()
        observers.append(mysql)
    if config.enable_log_file_writing:
        log = Log()
        observers.append(log)
    if config.enable_output_file:
        file = File()
        observers.append(file)

    for observer in observers:
        await subject.add_observer(observer)

    return subject


async def gather_offers(data, config, logger):
    logger.info("Starting XPath precision data extraction.")
    subject = await initialize_observers(config, logger)
    for item in data:
        tree = html.fromstring(item['source'])
        agroups = tree.xpath('/html/body/div/div/div/div/div/div/div/div/div/a')
        logger.info(f"Found {len(agroups)} offer nodes for category {item['category']}")
        for agroup in agroups:
            offer = await process_agroup(agroup, item['category'])
            if offer is not None:
                await subject.add_entry(offer)
    return True