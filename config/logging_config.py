import logging
from datetime import datetime


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# handler and formatter for logger
handler = logging.FileHandler(f"logs/{datetime.now().strftime('%Y_%m_%d')}.log")
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)

# print in console
logger.addHandler(logging.StreamHandler())
