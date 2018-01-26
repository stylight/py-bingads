#!/usr/bin/env python
""" Model for AdExtensionIdentity. """

# pylint: disable=redefined-builtin, invalid-name


class AdExtensionIdentity(object):
    """ Represent a single AdExtensionIdentity object """

    TYPE_NAME = 'AdExtensionIdentity'

    def __init__(self, id=None):
        """ Init. """
        self.id = id

    @property
    def key(self):
        """ Return the value that should be unique to this object. """
        return self.id

    def to_api_obj(self, service):
        """ Create Bing API AdExtensionIdentity object. """
        obj = service.factory.create(self.TYPE_NAME)
        obj.Id = self.id
        return obj

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse Bing API AdExtensionIdentity object. """
        return cls(
            id=obj.Id,
        )


class ArrayOfAdExtenionIdentity(object):
    """ Represent an array of AdExtensionIdentity objects. """

    TYPE_NAME = 'ArrayOfAdExtensionIdentity'

    def __init__(self, ad_extension_identities=None):
        """ Init. """
        self.ad_extension_identities = ad_extension_identities

    def __len__(self):
        return len(self.ad_extension_identities)

    def to_api_obj(self, service):
        """ Create Bing API object. """
        obj = service.factory.create(self.TYPE_NAME)
        for ad_extension_identities in self.ad_extension_identities:
            obj.AdExtensionIdentity.append(
                ad_extension_identities.to_api_obj(service)
            )
        return obj

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse Bing API object. """
        return [
            AdExtensionIdentity.from_api_obj(ad_extension_identity)
            for ad_extension_identity
            in obj.AdExtensionIdentities.AdExtensionIdentity
        ] if obj else []
