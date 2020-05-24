import os
import logging


# mode = os.getenv("MODE")
# TELEGRAM_ACCESS_TOKEN = os.getenv("TOKEN")
# mode = "prod" for heroku "dev" for running locally

mode = "prod" 
TELEGRAM_ACCESS_TOKEN = "938130802:AAH4rSWi5gY-rSxZlJHKY2j9j1_qYLhWR5k"
HEROKU_APP_NAME = "libgenesis-bot"
LIBGEN_DOMAIN = "https://libgen.is/"

# Enable logging
logging.basicConfig(format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
                    level=logging.INFO)

logger = logging.getLogger()
