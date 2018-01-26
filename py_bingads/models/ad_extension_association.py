#!/usr/bin/env python
""" Model for AdExtensionAssociation. """

# pylint: disable=redefined-builtin, invalid-name


class AdExtensionAssociation(object):
    """ Represent a single AdExtensionAssociation object """

    TYPE_NAME = 'AdExtensionAssociation'

    def __init__(self, ad_extension=None, association_type=None,
                 entity_id=None):
        """ Init. """
        self.ad_extension = ad_extension
        self.association_type = association_type
        self.entity_id = entity_id

    @property
    def key(self):
        """ Return the value that should be unique to this object. """
        return (self.ad_extension, self.entity_id)

    def to_api_obj(self, service):
        """ Create Bing API AdExtensionAssociation object. """
        obj = service.factory.create(self.TYPE_NAME)
        obj.AdExtension = self.ad_extension
        obj.AssociationType = self.association_type
        obj.EntityId = self.entity_id
        return obj

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse Bing API AdExtensionAssociation object. """
        return cls(
            ad_extension=obj.AdExtension,
            association_type=obj.AdExtension,
            entity_id=obj.EntityId,
        )


class ArrayOfAdExtenionAssociation(object):
    """ Represent an array of AdExtensionAssociation objects. """

    TYPE_NAME = 'ArrayOfAdExtensionAssociation'

    def __init__(self, ad_extension_associations=None):
        """ Init. """
        self.ad_extension_associations = ad_extension_associations

    def __len__(self):
        return len(self.ad_extension_associations)

    def to_api_obj(self, service):
        """ Create Bing API object. """
        obj = service.factory.create(self.TYPE_NAME)
        for ad_extension_association in self.ad_extension_associations:
            obj.AdExtensionAssociation.append(
                ad_extension_association.to_api_obj(service)
            )
        return obj

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse Bing API object. """
        return [
            AdExtensionAssociation.from_api_obj(ad_extension_association)
            for ad_extension_association
            in obj.AdExtensionAssociation.AdExtensionAssociation
        ] if obj else []
