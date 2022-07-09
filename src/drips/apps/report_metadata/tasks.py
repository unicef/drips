import logging

from django_countries import countries
from sharepoint_rest_api import config
from sharepoint_rest_api.client import SharePointClient

from drips.config.celery import app

from .models import AutocompleteMetadata

logger = logging.getLogger(__name__)

c = dict(countries)


@app.task
def load_ip_metadata(folder='2022_04_DRIPS'):
    load_autometadata(folder=folder, category=AutocompleteMetadata.IP)


@app.task
def load_bap_metadata(folder='2022_05_DRIPS'):
    load_autometadata(folder=folder, category=AutocompleteMetadata.BAP)


def load_autometadata(folder, category):
    client = SharePointClient(
        url=f'{config.SHAREPOINT_TENANT}/{config.SHAREPOINT_SITE_TYPE}/{config.SHAREPOINT_SITE}',
        folder=folder
    )
    items = client.read_items()
    for item in items:
        title = item.properties['Title']
        if title:
            AutocompleteMetadata.objects.get_or_create(code=title, category=category)
