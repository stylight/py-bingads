#!/usr/bin/env python
""" Model for AdExtensionIdToEntityIdAssociation. """

from py_bingads import _utils

# pylint: disable=redefined-builtin, invalid-name


class AdExtensionIdToEntityIdAssociation(object):
    """ Represent a single AdExtensionIdentity object """

    TYPE_NAME = 'AdExtensionIdToEntityIdAssociation'

    def __init__(self, ad_extension_id=None, entity_id=None):
        """ Init. """
        self.ad_extension_id = ad_extension_id
        self.entity_id = entity_id

    @property
    def key(self):
        """ Return the value that should be unique to this object. """
        return (self.ad_extension_id, self.entity_id)

    def to_api_obj(self, service):
        """ Create Bing API AdExtensionIdToEntityIdAssociation object. """
        obj = _utils.set_elements_to_none(
            service.factory.create(self.TYPE_NAME)
        )
        obj.AdExtensionId = self.ad_extension_id
        obj.EntityId = self.entity_id
        return obj

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse Bing API AdExtensionIdToEntityIdAssociation object. """
        return cls(
            ad_extension_id=obj.AdExtensionId,
            entity_id=obj.EntityId,
        )


class ArrayOfAdExtensionIdToEntityIdAssociation(object):
    """Represent an array of ArrayOfAdExtensionIdToEntityIdAssociation objects.
    """

    TYPE_NAME = 'ArrayOfAdExtensionIdToEntityIdAssociation'

    def __init__(self, ad_extension_id_to_entity_id_association=None):
        """ Init. """
        self.ad_extension_id_to_entity_id_association = \
            ad_extension_id_to_entity_id_association

    def __len__(self):
        return len(self.ad_extension_id_to_entity_id_association)

    def to_api_obj(self, service):
        """ Create Bing API object. """
        obj = service.factory.create(self.TYPE_NAME)
        for ad_extension_id_to_entity_id_association in \
                self.ad_extension_id_to_entity_id_association:
            obj.AdExtensionIdToEntityIdAssociation.append(
                ad_extension_id_to_entity_id_association.to_api_obj(service)
            )
        return obj

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse Bing API object. """
        # FIXME
        return [
            AdExtensionIdToEntityIdAssociation.from_api_obj(
                ad_extension_id_to_entity_id_association
            )
            for ad_extension_id_to_entity_id_association
            in obj.AdExtensionIdToEntityIdAssociation
        ] if obj else []
