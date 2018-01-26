#!/usr/bin/env python
""" Model for Campaign. """

from py_bingads import _utils

# pylint: disable=redefined-builtin, invalid-name


class Campaign(object):
    """ Represent a single Campaign object. """

    TYPE_NAME = 'Campaign'

    def __init__(self, id=None, name=None, status=None):
        """ Init. """
        self.id = id
        self.name = name
        self.status = status

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
    def from_api_obj(cls, obj):
        """ Parse Bing API object. """
        return cls(
            id=obj.Id,
            name=obj.Name,
            status=obj.Status,
        )


class ArrayOfCampaign(object):
    """ Represent an array of Campaign objects. """

    TYPE_NAME = 'ArrayOfCampaign'

    def __init__(self, campaigns=None):
        """ Init. """
        self.campaigns = campaigns

    def __len__(self):
        return len(self.campaigns)

    def to_api_obj(self, service):
        """ Create Bing API object. """
        obj = service.factory.create(self.TYPE_NAME)
        for campaign in self.campaigns:
            obj.Campaign.append(campaign.to_api_obj(service))
        return obj

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse Bing API object. """
        return [
            Campaign.from_api_obj(campaign) for campaign in obj.Campaign
        ] if obj else []
