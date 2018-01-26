#!/usr/bin/env python
""" Model for SharedEntityAssociation. """

# pylint: disable=redefined-builtin, invalid-name


class SharedEntityAssociation(object):
    """ Represent a single SharedEntityAssociation object """

    TYPE_NAME = 'SharedEntityAssociation'

    def __init__(self, entity_id=None, entity_type=None,
                 shared_entity_id=None, shared_entity_type=None):
        """ Init. """
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.shared_entity_id = shared_entity_id
        self.shared_entity_type = shared_entity_type

    def __eq__(self, other):
        return (
            self.entity_id == other.entity_id,
            self.entity_type == other.entity_type,
            self.shared_entity_id == other.shared_entity_id,
            self.shared_entity_type == other.shared_entity_type,
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def key(self):
        """ Return the value that should be unique to this object. """
        return (self.entity_id, self.entity_type, self.shared_entity_id,
                self.entity_type)

    def to_api_obj(self, service):
        """ Create Bing API SharedEntityAssociation object. """
        obj = service.factory.create(self.TYPE_NAME)
        obj.EntityId = self.entity_id
        obj.EntityType = self.entity_type
        obj.SharedEntityId = self.shared_entity_id
        obj.SharedEntityType = self.shared_entity_type
        return obj

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse Bing API SharedEntityAssociation object. """
        return cls(
            entity_id=obj.EntityId,
            entity_type=obj.EntityType,
            shared_entity_id=obj.SharedEntityId,
            shared_entity_type=obj.SharedEntityType,
        )


class ArrayOfSharedEntityAssociation(object):
    """ Represent an array of SharedEntityAssociation objects. """

    TYPE_NAME = 'ArrayOfSharedEntityAssociation'

    def __init__(self, shared_entity_associations=None):
        """ Init. """
        self.shared_entity_associations = shared_entity_associations

    def __len__(self):
        return len(self.shared_entity_associations)

    def to_api_obj(self, service):
        """ Create Bing API object. """
        obj = service.factory.create(self.TYPE_NAME)
        for shared_entity_association in self.shared_entity_associations:
            obj.SharedEntityAssociation.append(
                shared_entity_association.to_api_obj(service)
            )
        return obj

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse Bing API object. """
        return [
            SharedEntityAssociation.from_api_obj(shared_entity_association)
            for shared_entity_association
            in obj.Associations.SharedEntityAssociation
        ] if obj and obj.Associations else []
