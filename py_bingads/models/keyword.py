#!/usr/bin/env python
""" Model for Keyword. """

# pylint: disable=redefined-builtin, invalid-name


class Keyword(object):
    """ Represent a single Keyword object. """

    TYPE_NAME = 'Keyword'

    def __init__(self, id=None, text=None, match_type=None):
        """ Init. """
        self.id = id
        self.text = text
        self.match_type = match_type

    @property
    def key(self):
        """ Return the value that should be unique to this object. """
        return self.id

    def to_api_obj(self, service):
        """ Create Bing API object. """
        obj = service.factory.create(self.TYPE_NAME)
        obj.Id = self.id
        obj.Text = self.text
        obj.MatchType = self.match_type
        return obj

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse Bing API object. """
        return cls(
            id=obj.Id,
            text=obj.Text,
            match_type=obj.MatchType,
        )
