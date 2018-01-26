#!/usr/bin/env python
""" Model for SharedList. """

from . import shared_entity

# pylint: disable=redefined-builtin, invalid-name

class SharedList(shared_entity.SharedEntity):
    """ Represent a single SharedList object. """

    TYPE_NAME = 'SharedList'


class ArrayOfSharedList(shared_entity.ArrayOfSharedEntity):
    """ Represent an array of SharedList objects. """

    def __init__(self, shared_lists=None):
        shared_entity.ArrayOfSharedEntity.__init__(
            self, shared_entities=shared_lists
        )
