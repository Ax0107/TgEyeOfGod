#!/usr/bin/env python

"""
Добавить описание
"""

import datetime
import logging
import os
from colorlog import ColoredFormatter
from pathlib import Path

from config import PATH_TO_LOGS
from config import LOG_NAME_FORMAT, LOG_LEVEL, LOG_FORMAT, HANDLER


def logger(name):
    """
    Usage:
    from logger import Logger
    logger = Logger(name)
    """
    filename = LOG_NAME_FORMAT

    try:
        logging.basicConfig(
            filename=PATH_TO_LOGS + filename,
            level=LOG_LEVEL,
            format="%(asctime)s: %(name)s - %(" "levelname)s  | %(message)s",
        )
    except BaseException as e:
        print("Base except logger {}".format(e))

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    logging.root.setLevel(LOG_LEVEL)
    formatter = ColoredFormatter(LOG_FORMAT)
    if HANDLER is None:
        stream = logging.StreamHandler()
    else:
        stream = HANDLER
    stream.setLevel(LOG_LEVEL)
    stream.setFormatter(formatter)
    logger.addHandler(stream)
    p = os.path.abspath("systemdhooks")
    return logger
