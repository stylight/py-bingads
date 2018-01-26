#!/usr/bin/env python
""" Model for Ad. """

# pylint: disable=redefined-builtin, invalid-name


class Ad(object):
    """ Represent a single Ad object. """

    TYPE_NAME = 'Ad'

    def __init__(self, id=None, status=None):
        """ Init. """
        self.id = id
        self.status = status

    @property
    def key(self):
        """ Return the value that should be unique to this object. """
        return self.id

    def to_api_obj(self, service):
        """ Create Bing API object. """
        obj = service.factory.create(self.TYPE_NAME)
        obj.Id = self.id
        obj.Status = self.status
        return obj

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse Bing API object. """
        return cls(
            id=obj.Id,
            status=obj.Status,
        )

class ArrayOfAd(object):
    """ Represent an array of Ad objects. """

    TYPE_NAME = 'ArrayOfAd'

    def __init__(self, ads=None):
        """ Init. """
        self.ads = ads

    def __len__(self):
        return len(self.ads)

    def to_api_obj(self, service):
        """ Create Bing API object. """
        obj = service.factory.create(self.TYPE_NAME)
        for ad in self.ads:
            obj.Ad.append(ad.to_api_obj(service))
        return obj

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse Bing API object. """
        return [Ad.from_api_obj(ad) for ad in obj.Ad] if obj else []
