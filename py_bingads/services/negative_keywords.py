#!/usr/bin/env python
""" Wrapper class for Negative Keywords (Shared Entities). """
import itertools as _it
import logging as _logging

from py_bingads import _constants as _c
from py_bingads import _utils
from py_bingads import models as _models

from . import base as _base

_logging.basicConfig(level=_logging.INFO)

# pylint: disable=invalid-name


class NegativeKeywords(_base.BingAds):
    """ Wrapper for Negative Keywords service operations. """

    def __init__(self, **kwargs):
        """ Initialize NegativeKeywords. """
        _base.BingAds.__init__(self, **kwargs)
        self.shared_entity_type = _models.NegativeKeywordList.TYPE_NAME

    @_utils.print_webfault
    def get_negative_keyword_lists(self):
        """Gets the negative keyword lists from the account's library.

        https://msdn.microsoft.com/en-us/library/bing-ads-campaign-management-
        getsharedentitiesbyaccountid.aspx

        :rtype: [_models.NegativeKeyword]
        :return:
          Returned is a list of negative keywords from the account's shared
          library.
        """
        response = self.campaign_service.GetSharedEntitiesByAccountId(
            SharedEntityType=self.shared_entity_type
        )
        return _models.ArrayOfNegativeKeywordList.from_api_obj(response)

    @_utils.print_webfault
    def create_negative_keyword_list(self, list_name):
        """Creates a negative keyword list to the account's library.

        https://msdn.microsoft.com/en-us/library/bing-ads-campaign-management-
        addsharedentity.aspx

        :type list_name: str
        :param list_name:
          The name to give to the negative keyword list to add to the
          account's shared library.

        :rtype: _model.NegativeKeywordList
        :return:
          Returned is the negative keyword shared entity.
        """
        existing_lists = self.get_negative_keyword_lists()
        for existing_list in existing_lists:
            if list_name == existing_list.name:
                return _models.NegativeKeywordList(id=existing_list.id,
                                                   name=existing_list.name)

        response = self.campaign_service.AddSharedEntity(
            SharedEntity=_models.NegativeKeywordList(
                name=list_name
            ).to_api_obj(self.campaign_service)
        )
        return _models.NegativeKeywordList(id=response.SharedEntityId,
                                           name=list_name)

    @_utils.print_webfault
    def delete_negative_keyword_lists(self, list_ids):
        """Deletes negative keyword lists from the account's library.

        :type list_ids: [int]
        :param list_ids:
          The IDs of the negative keyword lists to delete from the account's
          shared library.
        """
        if not list_ids:
            return
        negative_keyword_lists = [
            _models.NegativeKeywordList(id=list_id) for list_id in list_ids
        ]
        array_of_negative_keyword_lists = _models.ArrayOfNegativeKeywordList(
            negative_keyword_lists=negative_keyword_lists
        ).to_api_obj(self.campaign_service)
        self.campaign_service.DeleteSharedEntities(
            SharedEntities=array_of_negative_keyword_lists
        )

    def delete_negative_keyword_list(self, list_id):
        """Deletes a negative keyword list from the account's library.

        :type list_id: int
        :param list_id:
          The ID of the negative keyword list to delete from the account's
          shared library.
        """
        self.delete_negative_keyword_lists([list_id])

    @_utils.print_webfault
    def get_negative_keywords(self, list_id):
        """Gets the negative keywords of a negative keyword list.

        https://msdn.microsoft.com/en-us/library/bing-ads-campaign-management-
        getlistitemsbysharedlist.aspx

        :type list_id: int
        :param list_id:
          The ID of the negative keyword list within the account's shared
          library, from which to get the negative keywords.

        :rtype: [_models.NegativeKeyword]
        :return:
          The list of negative keywords. If no negative keywords exist in
          the negative keyword list, an empty list is returned.
        """
        # TODO: Test
        response = self.campaign_service.GetListItemsBySharedList(
            SharedList=_models.NegativeKeywordList(id=list_id).to_api_obj(
                self.campaign_service
            )
        )
        return _models.ArrayOfNegativeKeyword.from_api_obj(response)

    @_utils.print_webfault
    def add_list_items_to_shared_list(self, shared_list=None, list_items=None):
        """Adds list items to shared list.

        https://msdn.microsoft.com/en-us/library/bing-ads-campaign-management-
        addlistitemstosharedlist.aspx

        :type shared_list: _models.SharedList
        :param shared_list:
          The shared list to add to the account's shared library.

        :type list_items: _models.ArrayOfSharedListItem
        :param list_items:
          The list items to add to the shared list. The list
          can contain a maximum of 5,000 items.

        :rtype: [int]
        :return:

        """
        # TODO: Test
        if len(list_items) > 0:
            response = self.campaign_service.AddListItemsToSharedList(
                SharedList=shared_list.to_api_obj(self.campaign_service),
                ListItems=list_items.to_api_obj(self.campaign_service),
            )
            # FIXME: make pythonic
            return response.ListItemIds.long
        return []

    def add_negative_keywords(self, list_id, negative_keywords):
        """Adds a list of negative keywords to a negative keyword list.

        :type list_id: int
        :param list_id:
          The ID of the negative keyword list for which to add the keywords to.

        :type negative_keywords: [_models.NegativeKeyword]
        :param negative_keywords:

        :returns: A list of IDs of the created negative keywords
        """
        negative_keyword_list = _models.NegativeKeywordList(id=list_id)
        array_of_negative_keyword = _models.ArrayOfNegativeKeyword(
            negative_keywords=negative_keywords
        )
        return self.add_list_items_to_shared_list(
            shared_list=negative_keyword_list,
            list_items=array_of_negative_keyword
        )

    @_utils.print_webfault
    def delete_list_items_from_shared_list(self, shared_list=None,
                                           list_item_ids=None):
        """Deletes list items from a shared list.

        :type shared_list: _models.SharedList
        :param shared_list:
          The shared list from which to delete items from the account's shared
          library.

        :type list_item_ids: [int]
        :param list_item_ids:
          The list of identifiers of negative keywords to delete from the
          negative keyword list.
        """
        # TODO: Test
        self.campaign_service.DeleteListItemsFromSharedList(
            SharedList=shared_list, ListItemIds=dict(long=list_item_ids)
        )

    def delete_negative_keywords(self, list_id, keyword_ids):
        """Deletes negative keywords.

        :type list_id: int
        :param list_id:
          The ID of the negative keyword list for which to delete the
          keywords from.

        :type keyword_ids: [int]
        :param keyword_ids:
          The list of identifiers of negative keywords to delete from the
          negative keyword list.
        """
        # TODO: Test
        if not keyword_ids:
            return
        self.delete_list_items_from_shared_list(
            shared_list=_models.NegativeKeywordList(id=list_id).to_api_obj(
                self.campaign_service
            ),
            list_item_ids=keyword_ids
        )

    @_utils.print_webfault
    def set_shared_entity_associations(self, associations):
        """Sets the association between a campaign and a negative keyword list.

        :type associations: [_models.SharedEntityAssociation]
        :param associations:
          The list of campaign and negative keyword list associations
        """
        # TODO: Test
        request_limit = 10000
        for associations_chunk in _utils.chunked(
                associations, chunk_size=request_limit):
            self.campaign_service.SetSharedEntityAssociations(
                Associations=_models.ArrayOfSharedEntityAssociation(
                    shared_entity_associations=associations_chunk
                ).to_api_obj(self.campaign_service)
            )

    def assign_negative_keyword_lists(self):
        """Assign all negative keyword lists to all campaigns in account.
        """
        # TODO: Test
        associations = []
        campaigns = self.get_campaigns()
        negative_keyword_lists = self.get_negative_keyword_lists()

        if not campaigns or not negative_keyword_lists:
            return

        for campaign, negative_keyword_list in _it.product(
                campaigns, negative_keyword_lists):
            associations.append(
                _models.SharedEntityAssociation(
                    entity_id=campaign.id,
                    entity_type=_c.CAMPAIGN,
                    shared_entity_id=negative_keyword_list.id,
                    shared_entity_type=self.shared_entity_type,
                )
            )

        self.set_shared_entity_associations(associations)

    @_utils.print_webfault
    def get_shared_entity_associations_by_shared_entity_id(self,
                                                           shared_entity_id):
        """Gets shared entity associations for the specified shared entity
        IDs.

        https://docs.microsoft.com/en-us/bingads/campaign-management-service
        /getsharedentityassociationsbysharedentityids

        :type shared_entity_id: int
        :param shared_entity_id:
          The ID of the negative keyword list for which to return
          associations with campaigns.

        :type associations: [_models.SharedEntityAssociation]
        :param associations:
          The list of campaign and shared entity associations.
        """
        response = self.campaign_service.\
        GetSharedEntityAssociationsBySharedEntityIds(
            EntityType=_c.CAMPAIGN,
            SharedEntityIds=_models.ArrayOflong(
                longs=[shared_entity_id]
            ).to_api_obj(),
            SharedEntityType=self.shared_entity_type,
        )
        return _models.ArrayOfSharedEntityAssociation.from_api_obj(response)

    def get_negative_keyword_list_associations(self, list_id):
        """Gets negative keyword list to campaign associations.

        :type list_id: int
        :param list_id:
          The ID of the negative keyword list for which to return
          associations with campaigns.

        :type associations: [_models.SharedEntityAssociation]
        :param associations:
          The list of campaign and negative keyword list associations
        """
        return self.get_shared_entity_associations_by_shared_entity_id(list_id)

    @_utils.print_webfault
    def delete_shared_entity_associations(self, associations):
        """Removes the association between a shared entity and an
        entity such as a campaign.

        https://docs.microsoft.com/en-us/bingads/campaign-management-service/
        deletesharedentityassociations

        :type associations: [_models.SharedEntityAssociation]
        :param associations:
          An array of objects that associate a negative keyword list and an
          entity such as a campaign.
        """
        self.campaign_service.DeleteSharedEntityAssociations(
            Associations=_models.ArrayOfSharedEntityAssociation(
                shared_entity_associations=associations
            ).to_api_obj(self.campaign_service)
        )

    def delete_negative_keyword_list_associations(self, list_id):
        """Removes the association between a negative keyword list and an
        entity such as a campaign.

        :type list_id: int
        :param list_id:
          The ID of the negative keyword list for which to delete
          associations with campaigns.
        """
        associations = self.get_negative_keyword_list_associations(list_id)
        if associations:
            self.delete_shared_entity_associations(associations)
