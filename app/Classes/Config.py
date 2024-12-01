import os
from dotenv import load_dotenv

class Config:
    urls = None
    db_url = None
    mode = None
    max_workers = None
    logging_level = None
    max_retries = None
    timeout = None
    sleep_after_scroll = None
    sleep_before_scroll = None
    sleep_after_screenshot = None
    sleep_after_close_popup = None
    use_route_intercept = None
    take_screenshots = None
    browserless_connection_string = None
    output_file = None
    enable_query_logging = None

    #observers
    enable_database_writing = None
    enable_console_output = None
    enable_log_file_writing = None
    enable_context_rewards = None
    enable_output_file = None

    def __init__(self):
        self.load_env_file()
        self.load_scraper_config()

    def load_env_file(self):
        load_dotenv()
        # ints
        self.max_workers = int(os.getenv("MAX_WORKERS"))
        self.sleep_after_scroll = int(os.getenv("SLEEP_AFTER_SCROLL"))
        self.max_retries = int(os.getenv("MAX_RETRIES"))
        self.timeout = int(os.getenv("TIMEOUT"))
        self.sleep_before_scroll = int(os.getenv("SLEEP_BEFORE_SCROLL"))
        self.sleep_after_screenshot = int(os.getenv("SLEEP_AFTER_SCREENSHOT"))
        self.sleep_after_close_popup = int(os.getenv("SLEEP_AFTER_CLOSE_POPUP"))

        # string
        self.logging_level = os.getenv("LOGGING_LEVEL")
        self.browserless_connection_string = os.getenv("BROWSERLESS_CONNECTION_STRING")
        self.output_file = os.getenv("OUTPUT_FILE")
        self.mode = os.getenv("MODE")
        self.db_url = os.getenv("DB_URL")
        self.enable_context_rewards = os.getenv("ENABLE_CONTEXT_REWARDS")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY")
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_s3_bucket_name = os.getenv('AWS_S3_BUCKET_NAME')
        self.screenshot_storage_type = os.getenv("SCREENSHOT_STORAGE_TYPE")
        self.screenshot_path = os.getenv("SCREENSHOT_PATH")

        # bool
        if os.getenv("USE_ROUTE_INTERCEPT") == "True":
            self.use_route_intercept = True
        else:
            self.use_route_intercept = False
        if os.getenv("TAKE_SCREENSHOTS") == "True":
            self.take_screenshots = True
        else:
            self.take_screenshots = False
        if os.getenv("ENABLE_DATABASE_WRITING") == "True":
            self.enable_database_writing = True
        else:
            self.enable_database_writing = False
        if os.getenv("ENABLE_CONSOLE_OUTPUT") == "True":
            self.enable_console_output = True
        else:
            self.enable_console_output = False
        if os.getenv("ENABLE_LOG_FILE_WRITING") == "True":
            self.enable_log_file_writing = True
        else:
            self.enable_log_file_writing = False
        if os.getenv("ENABLE_OUTPUT_FILE") == "True":
            self.enable_output_file = True
        else:
            self.enable_output_file = False
        if os.getenv("ENABLE_QUERY_LOGGING") == "True":
            self.enable_query_logging = True
        else:
            self.enable_query_logging = False


    def load_scraper_config(self):
        with open('app/config.txt', 'r') as f:
            self.urls = [line.strip() for line in f.readlines()]