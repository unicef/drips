from django import template
from django.utils.html import format_html

from drips import NAME, VERSION

register = template.Library()


@register.simple_tag
def version():
    return format_html("{}: v{}", NAME, VERSION)
