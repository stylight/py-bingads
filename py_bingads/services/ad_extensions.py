# -*- coding: utf-8 -*-
""" Wrapper class for Ad Extensions. """
import collections as _collections
import logging as _logging

from py_bingads import _constants as _c
from py_bingads import _utils
from py_bingads import models as _models

from . import base as _base

_logging.basicConfig(level=_logging.INFO)


class AdExtensions(_base.BingAds):
    """ Wrapper for Ad Extensions service operations. """

    def __init__(self, **kwargs):
        """ Initialize AdExtensions. """
        self.ad_extension_class = None
        _base.BingAds.__init__(self, **kwargs)

    @_utils.print_webfault
    def get_ad_extensions_by_ids(self, ad_extension_ids):
        """Gets the specified ad extensions from the account's ad extension
        library.

        https://msdn.microsoft.com/en-us/library/bing-ads-campaign-
        management-getadextensionsbyids.aspx

        :type ad_extension_ids: [int]
        :param ad_extension_ids:
          A list of ad extension identifiers. You can specify a maximum of
          100 identifiers.

        :rtype: [_models.AdExtension]
        :return:
          Returned is a list of existing AdExtension objects.
        """
        if not ad_extension_ids:
            return []

        ad_extensions = []
        for ad_extension_ids_chunk in _utils.chunked(
                ad_extension_ids, chunk_size=self.predicate_list_limit):
            response = self.campaign_service.GetAdExtensionsByIds(
                AccountId=self.authorization_data.account_id,
                AdExtensionIds=_models.ArrayOflong(
                    ad_extension_ids_chunk
                ).to_api_obj(),
                AdExtensionType=self.ad_extension_class.TYPE_NAME,
            )
            ad_extensions.extend(
                _models.ArrayOfAdExtension.from_api_obj(
                    response, ad_extension_class=self.ad_extension_class
                )
            )

        return ad_extensions

    @_utils.print_webfault
    def get_ad_extension_ids_by_account_id(self, # pylint: disable=invalid-name
                                           association_type=None):
        """Gets the ad extension IDs from the account's ad extension library.

        https://msdn.microsoft.com/en-us/library/bing-ads-campaign-
        management-getadextensionidsbyaccountid.aspx

        :type ad_extension_class: class
        :param ad_extension_class:
          A list of ad extension identifiers. You can specify a maximum of
          100 identifiers.

        :type association_type: str
        :param association_type:
          A value that filters the extensions based on whether they're
          associated with a specific entity type.

        :rtype: [int]
        :return:
          Returns list of ad extension IDs for type and association for this
          account.
        """
        response = self.campaign_service.GetAdExtensionIdsByAccountId(
            AccountId=self.authorization_data.account_id,
            AdExtensionType=self.ad_extension_class.TYPE_NAME,
            AssociationType=association_type,
        )
        return _models.ArrayOflong.from_api_obj(response)

    @_utils.print_webfault
    def get_ad_extensions_associations(self,
                                       association_type=None, entity_ids=None):
        """Gets the respective ad extension associations by the specified
        campaign and ad group identifiers.

        https://msdn.microsoft.com/en-us/library/bing-ads-campaign-
        management-getadextensionsassociations.aspx

        :type association_type: str
        :param association_type:
          A value that filters the extensions based on whether they're
          associated with a specific entity type.

        :type entity_ids: [int]
        :param entity_ids:
          The list of entity identifiers by which you may request the
          respective ad extension associations.

        :rtype: dict
        :return:
          Returned is a dict keyed on an entity ID with values of the
          given association type's list of corresponding ad extensions as per
          the given ad extension type.
        """
        _utils.validate_membership(association_type, _c.ASSOCIATION_TYPES,
                                   name='association_type')
        if not entity_ids:
            return {}

        associations = _collections.defaultdict(list)
        for entity_ids_chunk in _utils.chunked(
                entity_ids, chunk_size=self.predicate_list_limit):
            response = self.campaign_service.GetAdExtensionsAssociations(
                AccountId=self.authorization_data.account_id,
                AdExtensionType=self.ad_extension_class.TYPE_NAME,
                AssociationType=association_type,
                EntityIds=_models.ArrayOflong(entity_ids_chunk).to_api_obj(),
            )

            # TODO: refactor using model
            for assoc_list in response.AdExtensionAssociationCollection[0]:
                if not assoc_list.AdExtensionAssociations:
                    continue
                assoc = (assoc_list
                         .AdExtensionAssociations.AdExtensionAssociation[0])
                associations[assoc.EntityId].append(
                    self.ad_extension_class.from_api_obj(assoc.AdExtension)
                )

        return associations

    @_utils.print_webfault
    def update_ad_extensions(self, ad_extensions):
        """Updates one or more ad extensions within an account’s ad extension
        library.

        https://msdn.microsoft.com/en-us/library/bing-ads-campaign-management-
        updateadextensions.aspx

        :type ad_extensions: iter
        :param ad_extensions:
          The list of ad extensions of any type, to update within the
          account. You may specify a maximum of 100 extensions per call.
        """
        assert len(ad_extensions) <= self.predicate_list_limit, (
            '`ad_extensions` too long. Must be less than the defined '
            '`predicate_list_limit`: {predicate_list_limit}'.format(
                predicate_list_limit=self.predicate_list_limit
            )
        )
        if not ad_extensions:
            return []

        self.campaign_service.UpdateAdExtensions(
            AccountId=self.authorization_data.account_id,
            AdExtensions=ad_extensions.to_api_obj(self.campaign_service),
        )

    @_utils.print_webfault
    def add_ad_extensions(self, ad_extensions):
        """Adds one or more ad extensions to an account’s ad extension library.

        https://msdn.microsoft.com/en-us/library/bing-ads-campaign-management-
        addadextensions.aspx

        :type ad_extensions: _models.ArrayOfAdExtension
        :param ad_extensions:
          The array of ad extensions of any type to add to the
          account. You can specify a maximum of 100 extensions per call.

        :rtype: [_models.AdExtensionIdentity]
        :return:
          Returned is a list of ad extension identities of added ad extensions.
        """
        if not ad_extensions:
            return []

        response = self.campaign_service.AddAdExtensions(
            AccountId=self.authorization_data.account_id,
            AdExtensions=ad_extensions.to_api_obj(self.campaign_service)
        )
        return _models.ArrayOfAdExtenionIdentity.from_api_obj(response)

    @_utils.print_webfault
    def set_ad_extensions_associations(self, associations=None,
                                       association_type=None):
        """Associates the specified ad extensions with the respective campaigns
        or ad groups.

        https://msdn.microsoft.com/en-us/library/bing-ads-campaign-management-
        setadextensionsassociations.aspx

        :type associations: ArrayOfAdExtensionIdToEntityIdAssociation
        :param associations:
          The list of ad extensions with associated account, campaign, or
          ad group. You can only associate ad extensions with one type of
          entity per service call. Specify the entity type with the
          AssociationType element.

        :type association_type: str
        :param association_type:
          The type of all entities specified in the
          AdExtensionIdToEntityIdAssociations list.

        :rtype:
        :return:
        """
        _utils.validate_membership(association_type, _c.ASSOCIATION_TYPES,
                                   name='association_type')
        self.campaign_service.SetAdExtensionsAssociations(
            AccountId=self.authorization_data.account_id,
            AdExtensionIdToEntityIdAssociations=associations,
            AssociationType=association_type,
        )

    @_utils.print_webfault
    def associate_campaign_ad_extensions(self,  # pylint: disable=invalid-name
                                         associations):
        """Associate associations of campaign IDs to ad extension IDs.

        :type associations: [(int, int)]
        :param associations:
          List of tuples in which each tuple contains a campaign ID and an
          ad extension ID.
        """
        for associations_chunk in _utils.chunked(
                associations, chunk_size=self.predicate_list_limit):
            association_array = []
            for campaign_id, ad_extension_id in associations_chunk:
                association = _models.AdExtensionIdToEntityIdAssociation(
                    ad_extension_id=ad_extension_id,
                    entity_id=campaign_id
                )
                association_array.append(association)

            self.set_ad_extensions_associations(
                associations=_models.ArrayOfAdExtensionIdToEntityIdAssociation(
                    association_array
                ).to_api_obj(self.campaign_service),
                association_type=_c.CAMPAIGN
            )

    @_utils.print_webfault
    def delete_ad_extensions(self, ad_extension_ids):
        """Deletes one or more ad extensions from the account’s ad
        extension library.

        :type ad_extension_ids: [int]
        :param ad_extension_ids:
          The identifiers of the extensions to delete.
        """
        if not ad_extension_ids:
            return

        for ids_chunked in _utils.chunked(
                ad_extension_ids, chunk_size=self.predicate_list_limit):
            self.campaign_service.DeleteAdExtensions(
                AccountId=self.authorization_data.account_id,
                AdExtensionIds=_models.ArrayOflong(
                    longs=ids_chunked
                ).to_api_obj()
            )
