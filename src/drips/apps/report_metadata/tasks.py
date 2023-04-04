import logging

from django_countries import countries
from sharepoint_rest_api import config
from sharepoint_rest_api.client import SharePointClient

from drips.config.celery import app

from .models import AutocompleteMetadata

logger = logging.getLogger(__name__)

c = dict(countries)


def load_autometadata(folder, category):
    client = SharePointClient(
        url=f"{config.SHAREPOINT_TENANT}/{config.SHAREPOINT_SITE_TYPE}/{config.SHAREPOINT_SITE}", folder=folder
    )
    items = client.read_items()
    for item in items:
        title = item.properties["Title"]
        if title:
            AutocompleteMetadata.objects.get_or_create(code=title, category=category)


@app.task
def load_ip_metadata(folder="IP No"):
    load_autometadata(folder=folder, category=AutocompleteMetadata.IP)


@app.task
def load_bap_metadata(folder="BAP Document No"):
    load_autometadata(folder=folder, category=AutocompleteMetadata.BAP)


@app.task
def load_responsible_person_metadata(folder="Responsible Person"):
    load_autometadata(folder=folder, category=AutocompleteMetadata.RESPONSIBLE_PERSON)


@app.task
def load_uploaded_by_metadata(folder="Uploaded By"):
    load_autometadata(folder=folder, category=AutocompleteMetadata.UPLOADED_BY)
