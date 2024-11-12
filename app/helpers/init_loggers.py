import logging
from rich.logging import RichHandler
import pathlib
from datetime import datetime

def logify(level):
    # create the logger
    logger = logging.getLogger("scraperak")

    # set the level
    if level == "debug":
        print("initializing logger with debug level")
        logger.setLevel(logging.DEBUG)
    elif level == "info":
        print("initializing logger with info level")
        logger.setLevel(logging.INFO)
    else:
        print("initializing logger with debug level")
        logger.setLevel(logging.ERROR)

    date_for_log = datetime.now().strftime('%Y-%m-%d_%H')
    log_filename = f"/logs/{date_for_log}_scraperak.log"

    # create file and rich (for console) handlers
    path = str(pathlib.Path().resolve())
    file_handler = logging.FileHandler(path + log_filename)
    console_handler = RichHandler(rich_tracebacks=True)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # assign formatter to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger