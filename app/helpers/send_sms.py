import telnyx
import os
import traceback

def send_sms(to, message):
    mode = os.getenv('MODE')

    try:
        telnyx.api_key = os.getenv('TELNYX_API_KEY')
    except:
        print("There are no API keys for Telnyx configred. Please do so and try again!")

    if mode == "dev":
        pass
    else:
        telnyx.Message.create(
            from_=os.getenv('TELNYX_FROM_NUMBER'),
            to=to,
            text=message,
        )

def notify_admins(message):
    destination_numbers = os.getenv('PHONE_NUMBERS').split(",")

    for number in destination_numbers:
        send_sms(number, message)


def send_sms_report(runtime, report, results, counter, logger):
    try:
        msg = "TrackRak Scan Report\n\
1 of 4: ScrapeRak\n\
\n\
Finished in: " +str(runtime) + "\n\
Threads: "+ os.getenv("MAX_WORKERS") + "\n\
Categories Scraped: " + str(len(report.keys())) + "\n\
Offers Found: " + str(len(results)) + "\n\
Offers Processed: " + str(counter.total_offers_processed) + "\n\
Scrape failures: " + str(counter.get_scrape_failures())
        notify_admins(msg)
    except Exception as e:
        logger.error(f"An error using the telnyx API: {e}")
        print("[bold red]" + traceback.format_exc() + "[/bold red]")

        msg = "There was a problem using the telnyx API: \n\npython stack trace:\n" + traceback.format_exc()
        notify_admins(msg)
