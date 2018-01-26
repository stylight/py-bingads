#!/usr/bin/env python
""" Model for Account. """

# pylint: disable=redefined-builtin, invalid-name


class Account(object):
    """ Represent a single Account object. """

    TYPE_NAME = 'Account'

    def __init__(self, id, name, number, language):
        """ Init. """
        self.id = id
        self.name = name
        self.number = number
        self.language = language

    @property
    def key(self):
        """ Return the value that should be unique to this object.  """
        return self.id

    def to_api_obj(self, service):
        """ Create Bing API object. """
        obj = service.factory.create(self.TYPE_NAME)
        obj.Id = self.id
        obj.Name = self.name
        obj.Number = self.number
        obj.Language = self.language
        return obj

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse Bing API object. """
        return cls(
            id=obj.Id,
            name=obj.Name,
            number=obj.Number,
            language=obj.Language,
        )
