import os
import logging

# mode = "prod" for heroku "dev" for running locally

mode = "prod" 
TELEGRAM_ACCESS_TOKEN = ""
HEROKU_APP_NAME = ""
LIBGEN_DOMAIN = "https://libgen.is/"

# Enable logging
logging.basicConfig(format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
                    level=logging.INFO)

logger = logging.getLogger()
