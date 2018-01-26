#!/usr/bin/env python
""" Model for ReviewAdExtension. """

# pylint: disable=redefined-builtin, invalid-name


class ReviewAdExtension(object):
    """ Represent a single review extension object """

    TYPE_NAME = 'ReviewAdExtension'

    def __init__(self, id=None, format=None, text=None, source=None,
                 source_url=None):
        self.id = id
        self.format = format
        self.text = text
        self.source = source
        self.source_url = source_url

    def __repr__(self):
        return '[{id}] {key}'.format(id=self.id, key=self.key)

    def __eq__(self, other):
        return self.key == other.key

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def key(self):
        """ Return the value that should be unique to this review (not ID) """
        return (self.format, self.text, self.source, self.source_url)

    def to_api_obj(self, service):
        """ Create bing API review object """
        obj = service.factory.create(self.TYPE_NAME)
        obj.IsExact = (self.format == 'exact quote')
        obj.Text = self.text
        obj.Source = self.source
        obj.Url = self.source_url
        obj.Status = None
        return obj

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse bing API review object """
        return cls(
            id=obj.Id,
            format='exact quote' if obj.IsExact else 'paraphrased',
            text=obj.Text,
            source=obj.Source,
            source_url=obj.Url,
        )
