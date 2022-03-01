import operator
from contextlib import ContextDecorator
from functools import reduce
from random import choice

from django.contrib.auth.models import Group, Permission
from django.db.models import Q

from faker import Faker

whitespace = ' \t\n\r\v\f'
lowercase = 'abcdefghijklmnopqrstuvwxyz'
uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters = lowercase + uppercase
ascii_lowercase = lowercase
ascii_uppercase = uppercase
ascii_letters = ascii_lowercase + ascii_uppercase

faker = Faker()


def text(length, choices=ascii_letters):
    """ returns a random (fixed length) string

    :param length: string length
    :param choices: string containing all the chars can be used to build the string

    .. seealso::
       :py:func:`rtext`
    """
    return ''.join(choice(choices) for x in range(length))
