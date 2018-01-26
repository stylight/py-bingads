#!/usr/bin/env python
""" Model for long. """

# pylint: disable=redefined-builtin, invalid-name


class Long(object):
    """ Represent a single long object """

    TYPE_NAME = 'long'

    def __init__(self, long=None):
        """ Init. """
        self.long = long

    def to_api_obj(self):
        """ Create Bing API long object. """
        return self.long

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse Bing API long object. """
        return int(obj.long)


class ArrayOflong(object):
    """ Represent an array of long objects. """

    TYPE_NAME = 'ArrayOflong'

    def __init__(self, longs=None):
        """ Init. """
        self.longs = longs

    def __len__(self):
        return len(self.longs)

    def to_api_obj(self):
        """ Create Bing API object. """
        return dict(long=self.longs)

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse Bing API object. """
        return [long for long in obj.long] if obj else []
