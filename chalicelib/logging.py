import logging, sys
from chalicelib import config

app_name = config.app_name
def setup_custom_logger():
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(screen_handler)
    return logger