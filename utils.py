import re
from sqlalchemy import Column, Integer, ForeignKey


def merge_dicts(*args):
    result = {}
    for d in args:
        if not isinstance(d, dict):
            raise TypeError("Expected dictionary, got type {}".format(type(d)))
        result.update(d)
    return result


def camel_to_underscore(name):
    """
    See here: http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case

    >>> camel_to_underscore('CamelCase')
    'camel_case'
    >>> camel_to_underscore('CamelCamelCase')
    'camel_camel_case'
    >>> camel_to_underscore('Camel2Camel2Case')
    'camel2_camel2_case'
    >>> camel_to_underscore('getHTTPResponseCode')
    'get_http_response_code'
    >>> camel_to_underscore('get2HTTPResponseCode')
    'get2_http_response_code'
    >>> camel_to_underscore('HTTPResponseCode')
    'http_response_code'
    >>> camel_to_underscore('HTTPResponseCodeXYZ')
    'http_response_code_xyz'

    """

    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def foreignkey(fk, *args, **kwargs):
    """
    Convenience method to establish FK relationship
    """
    return Column(Integer, ForeignKey(fk), *args, **kwargs)
