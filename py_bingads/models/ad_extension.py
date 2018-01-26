# -*- coding: utf-8 -*-
""" Model for AdExtension. """

# pylint: disable=redefined-builtin, invalid-name


class AdExtension(object):
    """ Represent a single AdExtension object """

    TYPE_NAME = 'AdExtension'

    def __init__(self, id=None, text=None):
        """ Init. """
        self.id = id
        self.text = text

    @property
    def key(self):
        """ Return the value that should be unique to this object. """
        return self.text

    def to_api_obj(self, service):
        """ Create Bing API AdExtension object. """
        raise NotImplementedError

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse Bing API AdExtension object. """
        return cls(
            id=obj.Id,
            text=obj.Text,
        )


class ArrayOfAdExtension(object):
    """ Represent an array of AdExtension objects. """

    TYPE_NAME = 'ArrayOfAdExtension'

    def __init__(self, id_=None, ad_extensions=None):
        """ Init. """
        self.id = id_
        self.ad_extensions = ad_extensions

    def __len__(self):
        return len(self.ad_extensions)

    def to_api_obj(self, service):
        """ Create Bing API object. """
        obj = service.factory.create(self.TYPE_NAME)
        # obj.Id = self.id
        for ad_extension in self.ad_extensions:
            obj.AdExtension.append(ad_extension.to_api_obj(service))
        return obj

    @classmethod
    def from_api_obj(cls, obj, ad_extension_class=AdExtension):
        """ Parse Bing API object. """
        return [
            ad_extension_class.from_api_obj(ad_extension)
            for ad_extension in obj.AdExtensions.AdExtension
        ] if obj else []
