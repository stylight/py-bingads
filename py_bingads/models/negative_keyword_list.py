#!/usr/bin/env python
""" Model for NegativeKeywordList. """

from . import shared_list

# pylint: disable=redefined-builtin, invalid-name


class NegativeKeywordList(shared_list.SharedList):
    """ Represent a single NegativeKeywordList object. """

    TYPE_NAME = 'NegativeKeywordList'

    @classmethod
    def from_api_obj(cls, obj, name=None):
        """ Parse Bing API object. """
        return cls(
            id=obj.Id,
            name=name or obj.Name,
        )

class ArrayOfNegativeKeywordList(shared_list.ArrayOfSharedList):
    """ Represent an array of NegativeKeywordList objects. """

    def __init__(self, negative_keyword_lists=None):
        shared_list.ArrayOfSharedList.__init__(
            self, shared_lists=negative_keyword_lists
        )

    @classmethod
    def from_api_obj(cls, obj, shared_entity_cls=NegativeKeywordList):
        """ Parse Bing API object. """
        return shared_list.ArrayOfSharedList.from_api_obj(
            obj, shared_entity_cls=shared_entity_cls
        )
