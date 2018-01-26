#!/usr/bin/env python
""" Model for NegativeKeyword. """

from py_bingads import _utils

from . import shared_list_item

# pylint: disable=redefined-builtin, invalid-name


class NegativeKeyword(shared_list_item.SharedListItem):
    """ Represent a single NegativeKeyword object. """
    # pylint: disable=arguments-differ

    TYPE_NAME = 'NegativeKeyword'

    def __init__(self, id=None, shared_set_id=None, text=None, match_type=None):
        """ Init. """
        shared_list_item.SharedListItem.__init__(self)
        self.id = id
        self.shared_set_id = shared_set_id
        self.text = text
        self.match_type = match_type.lower().capitalize()
        assert self.match_type in ('Exact', 'Phrase')

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.match_type == other.match_type
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def key(self):
        """ Return the value that should be unique to this object. """
        return self.id

    def to_api_obj(self, service):
        """ Create Bing API object. """
        obj = _utils.set_elements_to_none(
            service.factory.create(self.TYPE_NAME)
        )
        obj.Id = self.id
        # obj.SharedSetId = self.shared_set_id
        obj.Text = self.text
        obj.MatchType = self.match_type
        return obj

    @classmethod
    def from_api_obj(cls, obj, shared_set_id=None):
        """ Parse Bing API object. """
        return cls(
            id=obj.Id,
            shared_set_id=shared_set_id,
            text=obj.Text,
            match_type=obj.MatchType.upper(),
        )


class ArrayOfNegativeKeyword(shared_list_item.ArrayofSharedListItem):
    """ Represent an array of SharedEntity objects. """

    def __init__(self, negative_keywords=None):
        shared_list_item.ArrayofSharedListItem.__init__(
            self, shared_list_items=negative_keywords
        )

    @classmethod
    def from_api_obj(cls, obj, shared_list_item_cls=NegativeKeyword,
                     shared_set_id=None):
        """ Parse Bing API object. """
        return shared_list_item.ArrayofSharedListItem.from_api_obj(
            obj, shared_list_item_cls=shared_list_item_cls,
            shared_set_id=shared_set_id
        )
