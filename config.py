from dotenv import load_dotenv
import os
import logging

load_dotenv()

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")

USERNAME = os.environ.get("USERNAME")
PHONE = os.environ.get("PHONE")

BOT_TOKEN = os.environ.get('BOT_TOKEN')

PATH_TO_LOGS = './logs/'
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(log_color)s %(asctime)s %(name)s-%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
LOG_NAME_FORMAT = "%Y-%m-%d.log"
HANDLER = logging.StreamHandler()
