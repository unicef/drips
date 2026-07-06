import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def get_date(date_string, date_format="%d-%b-%y"):
    if date_string:
        return datetime.strptime(date_string, date_format)
    return None
