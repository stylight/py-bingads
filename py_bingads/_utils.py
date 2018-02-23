#!/usr/bin/env python
""" Random util functions. """
import functools as _ft
import itertools as _it
import logging as _logging

import suds as _suds

logger = _logging.getLogger(__name__)


def set_elements_to_none(suds_object):
    """Bing Ads Campaign Management service operations require that if you
    specify a non-primitives, it must be one of the values defined by the
    service i.e. it cannot be a nil element. Since Suds requires
    non-primitives and Bing Ads won't accept nil elements in place of an
    enum value, you must either set the non-primitives or they must be set
    to None. Also in case new properties are added in a future service
    release, it is a good practice to set each element of the SUDS object
    to None as a baseline.
    """
    for element in suds_object:
        suds_object.__setitem__(element[0], None)
    return suds_object


def get_refresh_token():
    """Returns a refresh token if stored locally.

    :rtype: str | None
    :return:
      Returned is the refresh token or None if not found.
    """
    with open('refresh.txt') as file:
        line = file.readline()
        return line if line else None


def validate_membership(item, group, name=None):
    """Assert that item is member of group.

    :type item: obj
    :param item:
      Object to check if member of group.

    :type group: iter
    :param group:
      Group for which to check item's membership.
    """
    assert item in group, (
        'Invalid `{name}`: `{item}`.'.format(name=name, item=item)
    )


def save_refresh_token(oauth_tokens):
    """Stores a refresh token locally. Be sure to save your refresh
    token securely.

    :param oauth_tokens:
    """
    with open('refresh.txt', 'w+') as file:
        file.write(oauth_tokens.refresh_token)


def chunked(iterable, chunk_size=32):
    """
    >>> list(chunked(range(9), 2))
    [[0, 1], [2, 3], [4, 5], [6, 7], [8]]

    >>> list(chunked(range(9), 0))
    Traceback (most recent call last):
    ...
    ValueError: `chunk_size` must be >= 1
    """
    if chunk_size < 1:
        raise ValueError('`chunk_size` must be >= 1')

    for _, grouped_chunk in _it.groupby(
            enumerate(iterable), key=lambda x, s=chunk_size: x[0] // s):
        yield [entry[1] for entry in grouped_chunk]


def print_webfault(func):
    """ Catches WebFaults, logs internal message, and re-raises. """
    @_ft.wraps(func)
    def wrapper(*args, **kw):
        """ Function wrapper """
        try:
            return func(*args, **kw)
        except _suds.WebFault as exp:
            logger.error(exp.fault.detail)
            try:
                raise RuntimeError(
                    exp.fault.detail.ApiFaultDetail.OperationErrors
                    .OperationError.Message
                )
            except AttributeError:
                raise RuntimeError('Unknown error message, please report to '
                                   'the engineering team')
    return wrapper


def merge(left, right, default=None):
    """Merge two iterators of tuples each which contains the merge key and
    the actual value.

    >>> list(merge([(1, 1)], [(1, 2), (2, 3)]))
    [(1, (1, 2)), (2, (None, 3))]

    >>> list(merge([(1, 2), (2, 3)], [(2, 4), (3, 5)]))
    [(1, (2, None)), (2, (3, 4)), (3, (None, 5))]

    >>> list(merge([(1, 2), (2, 3)], [(2, 4), (3, 5)], default='a'))
    [(1, (2, 'a')), (2, (3, 4)), (3, ('a', 5))]
    """
    left = {k: v for k, v in left}
    right = {k: v for k, v in right}
    keys = list(set().union(left.keys(), right.keys()))
    for key in keys:
        left_val = left.get(key) or default
        right_val = right.get(key) or default
        yield (key, (left_val, right_val))

