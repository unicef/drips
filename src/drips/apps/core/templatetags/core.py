from django import template
from django.utils.safestring import mark_safe

from drips import NAME, VERSION

register = template.Library()


@register.simple_tag
def version():
    return mark_safe('{}: v{}'.format(NAME, VERSION))
