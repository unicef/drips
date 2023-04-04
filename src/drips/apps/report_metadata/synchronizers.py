import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def get_date(date_string, format="%d-%b-%y"):
    if date_string:
        return datetime.strptime(date_string, format)
