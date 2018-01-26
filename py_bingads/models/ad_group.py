#!/usr/bin/env python
""" Model for AdGroup. """

from py_bingads import _utils

# pylint: disable=redefined-builtin, invalid-name

class AdGroup(object):
    """ Represent a single AdGroup object. """

    TYPE_NAME = 'AdGroup'

    def __init__(self, id=None, name=None, status=None, campaign_id=None):
        """ Init. """
        self.id = id
        self.name = name
        self.status = status
        self.campaign_id = campaign_id

    @property
    def key(self):
        """ Return the value that should be unique to this object. """
        return self.id

    def to_api_obj(self, service):
        """ Create Bing API object. """
        obj = _utils.set_elements_to_none(
            service.factory.create(self.TYPE_NAME)
        )
        obj.Id = self.id
        obj.Name = self.name
        obj.Status = self.status
        return obj

    @classmethod
    def from_api_obj(cls, obj, campaign_id=None):
        """ Parse Bing API object. """
        return cls(
            id=obj.Id,
            name=obj.Name,
            status=obj.Status,
            campaign_id=campaign_id,
        )

class ArrayOfAdGroup(object):
    """ Represent an array of AdGroup objects. """

    TYPE_NAME = 'ArrayOfAdGroup'

    def __init__(self, ad_groups=None):
        """ Init. """
        self.ad_groups = ad_groups

    def __len__(self):
        return len(self.ad_groups)

    def to_api_obj(self, service):
        """ Create Bing API object. """
        obj = service.factory.create(self.TYPE_NAME)
        for ad_group in self.ad_groups:
            obj.AdGroup.append(ad_group.to_api_obj(service))
        return obj

    @classmethod
    def from_api_obj(cls, obj, campaign_id=None):
        """ Parse Bing API object. """
        return [
            AdGroup.from_api_obj(ad_group, campaign_id=campaign_id)
            for ad_group in obj.AdGroup
        ] if obj else []
