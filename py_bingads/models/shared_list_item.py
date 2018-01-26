#!/usr/bin/env python
""" Model for SharedListItem. """

# pylint: disable=redefined-builtin, invalid-name


class SharedListItem(object):
    """Represent a single SharedListItem object.  Do not try to instantiate a
    SharedListItem. You can create the following object that derives from it.
    """

    TYPE_NAME = 'SharedListItem'

    def __init__(self, _type=None):
        """ Init. """
        self.type = _type

    def to_api_obj(self, service):
        """ Create Bing API object. """
        obj = service.factory.create(self.TYPE_NAME)
        obj.Type = self.type
        return obj

    @classmethod
    def from_api_obj(cls, obj):
        """ Parse Bing API object. """
        return cls(
            _type=obj.Type,
        )


class ArrayofSharedListItem(object):
    """ Represent an array of SharedEntity objects. """

    TYPE_NAME = 'ArrayOfSharedListItem'

    def __init__(self, shared_list_items=None):
        """ Init. """
        self.shared_list_items = shared_list_items

    def __len__(self):
        return len(self.shared_list_items)

    def to_api_obj(self, service):
        """ Create Bing API object. """
        obj = service.factory.create(self.TYPE_NAME)
        for shared_list_item in self.shared_list_items:
            obj.SharedListItem.append(shared_list_item.to_api_obj(service))
        return obj

    @classmethod
    def from_api_obj(cls, obj, shared_list_item_cls=SharedListItem,
                     shared_set_id=None):
        """ Parse Bing API object. """
        return [
            shared_list_item_cls.from_api_obj(
                shared_list_item, shared_set_id=shared_set_id
            )
            for shared_list_item in obj.SharedListItem
        ] if obj else []
