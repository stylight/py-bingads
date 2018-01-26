#!/usr/bin/env python
""" Model for Shared Entity. """

from py_bingads import _utils

# pylint: disable=redefined-builtin, invalid-name


class SharedEntity(object):
    """ Represent a single Shared Entity object. """

    TYPE_NAME = 'SharedEntity'

    def __init__(self, id=None, name=None):
        """ Init. """
        self.id = id
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def key(self):
        """ Return the value that should be unique to this object.  """
        return self.name

    def to_api_obj(self, service):
        """ Create Bing API object. """
        obj = _utils.set_elements_to_none(
            service.factory.create(self.TYPE_NAME)
        )
        obj.Id = self.id
        obj.Name = self.name
        obj.Type = self.TYPE_NAME
        return obj

    @classmethod
    def from_api_obj(cls, obj, name=None):
        """ Parse Bing API object. """
        return cls(
            id=obj.SharedEntityId,
            name=name,
        )


class ArrayOfSharedEntity(object):
    """ Represent an array of SharedEntity objects. """

    TYPE_NAME = 'ArrayOfSharedEntity'

    def __init__(self, shared_entities=None):
        """ Init. """
        self.shared_entities = shared_entities

    def __len__(self):
        return len(self.shared_entities)

    def to_api_obj(self, service):
        """ Create Bing API object. """
        obj = service.factory.create(self.TYPE_NAME)
        for shared_entity in self.shared_entities:
            obj.SharedEntity.append(shared_entity.to_api_obj(service))
        return obj

    @classmethod
    def from_api_obj(cls, obj, shared_entity_cls=SharedEntity):
        """ Parse Bing API object. """
        return [
            shared_entity_cls.from_api_obj(shared_entity)
            for shared_entity in obj.SharedEntity
        ] if obj else []
