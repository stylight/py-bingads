#!/usr/bin/env python
""" Model for CalloutAdExtension. """

from py_bingads import _utils

# pylint: disable=redefined-builtin, invalid-name


class CalloutAdExtension(object):
    """ Represent a single CalloutAdExtension object """

    TYPE_NAME = 'CalloutAdExtension'

    def __init__(self, id=None, text=None):
        """ Init. """
        self.id = id
        self.text = text

    def __repr__(self):
        return '[{id}] {key}'.format(id=self.id, key=self.key)

    def __eq__(self, other):
        return self.key == other.key

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def key(self):
        """ Return the value that should be unique to this object. """
        return self.text

    def to_api_obj(self, service):
        """ Create Bing API CalloutAdExtension object. """
        obj = _utils.set_elements_to_none(
            service.factory.create(self.TYPE_NAME)
        )
        obj.Text = self.text
        return obj

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse Bing API CalloutAdExtension object. """
        return cls(
            id=obj.Id,
            text=obj.Text,
        )
