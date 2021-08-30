from dotenv import load_dotenv
import os
import logging

load_dotenv()

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")

USERNAME = os.environ.get("USERNAME")
PHONE = os.environ.get("PHONE")

BOT_TOKEN = os.environ.get('BOT_TOKEN')
SECOND_BOT_TOKEN = os.environ.get('SECOND_BOT_TOKEN')

SPEC_REQUEST_PREFIX = '_M_'
SPEC_REQUEST_PREFIX_click = '_B_'
SPEQ_REQUEST_SPLITER = '|||'

PATH_TO_LOGS = './logs/'
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(log_color)s %(asctime)s %(name)s-%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
LOG_NAME_FORMAT = "%Y-%m-%d.log"
HANDLER = logging.StreamHandler()

