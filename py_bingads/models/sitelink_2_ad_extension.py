# -*- coding: utf-8 -*-
""" Model for Sitelink2AdExtension. """

from py_bingads import _constants as _c
from py_bingads import _utils

from . import AdExtension

# pylint: disable=redefined-builtin, invalid-name


class Sitelink2AdExtension(AdExtension):
    """ Represent a single Sitelink2AdExtension object. """

    TYPE_NAME = 'Sitelink2AdExtension'

    def __init__(self, id=None, display_text=None, final_url=None,
                 description1=None, description2=None, device_preference=None):
        """ Init. """
        AdExtension.__init__(self)
        self.id = id
        self.display_text = display_text
        self.final_url = final_url
        self.description1 = description1
        self.description2 = description2
        self.device_preference = device_preference or _c.ALL_DEVICES
        if bool(description1) != bool(description2):
            msg = (
                'Both description 1 and 2 must be set, or neither. '
                'Sitelink: %s' % str(self.key)
            )
            raise ValueError(msg)

    def __repr__(self):
        return '[{id}] {key}'.format(id=self.id, key=self.key)

    def __eq__(self, other):
        return (
            self.display_text == other.display_text and
            self.final_url == other.final_url and
            self.description1 == other.description1 and
            self.description2 == other.description2 and
            self.device_preference == other.device_preference
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def key(self):
        """ Return the value that should be unique to this object. """
        return (self.display_text, self.final_url)

    def to_api_obj(self, service):
        """ Create Bing API object. """
        obj = _utils.set_elements_to_none(
            service.factory.create(self.TYPE_NAME)
        )
        obj.Id = self.id
        obj.DisplayText = self.display_text
        obj.Description1 = self.description1
        obj.Description2 = self.description2
        if self.device_preference == _c.MOBILE:
            device_preference = _c.MOBILE_ID
        else:
            device_preference = _c.ALL_DEVICES_ID

        obj.DevicePreference = device_preference

        final_urls = service.factory.create('ns4:ArrayOfstring')
        final_urls.string.append(self.final_url)
        obj.FinalUrls = final_urls
        return obj

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse Bing API object. """
        device_preference = (
            _c.MOBILE
            if getattr(obj, _c.DEVICE_PREFERENCE, None)
            else _c.ALL_DEVICES
        )
        return cls(
            id=obj.Id,
            display_text=obj.DisplayText,
            final_url=obj.FinalUrls[0][0],
            description1=obj.Description1,
            description2=obj.Description2,
            device_preference=device_preference,
        )
