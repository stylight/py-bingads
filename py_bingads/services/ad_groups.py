#!/usr/bin/env python
""" Wrapper class for Ad Groups. """
import itertools as _it
import operator as _op

from py_bingads import _constants as _c
from py_bingads import _utils
from py_bingads import models as _models

from . import base as _base


class AdGroups(_base.BingAds):
    """ Wrapper for Ad Groups service operations. """

    def __init__(self, **kwargs):
        """ Initialize AdGroups. """
        _base.BingAds.__init__(self, **kwargs)

    @_utils.print_webfault
    def get_ad_groups_by_campaign_id(self, campaign_id):
        """Gets the ad groups within the specified campaign.

        https://msdn.microsoft.com/en-us/library/bing-ads-campaign-management-
        getad_groupsbycampaignid.aspx

        :type campaign_id: int
        :param campaign_id:
          The identifier of the campaign that contains the ad groups to get.

        :rtype: [_models.AdGroup]
        :return:
          The list of ad groups within the specified campaign. If the
          campaign contains no ad groups, an empty array is returned.
        """
        response = self.campaign_service.GetAdGroupsByCampaignId(
            CampaignId=campaign_id
        )
        return _models.ArrayOfAdGroup.from_api_obj(response,
                                                   campaign_id=campaign_id)

    @_utils.print_webfault
    def get_ads_by_ad_group_id(self, ad_group_id):
        """Retrieves the ads within an ad group.

        https://msdn.microsoft.com/en-us/library/bing-ads-campaign-management-
        getadsbyadgroupid.aspx

        :type ad_group_id: int
        :param ad_group_id:
          The identifier of the ad group to retrieve the ads from.

        :rtype: [_models.Ad]
        :return:
          The list of ads that have been retrieved. If the ad group doesn't
          contain ads, this array is empty.
        """
        response = self.campaign_service.GetAdsByAdGroupId(
            AdGroupId=ad_group_id,
            AdTypes=_c.ALL_AD_TYPES
        )
        return _models.ArrayOfAd.from_api_obj(response)

    @_utils.print_webfault
    def update_ad_groups(self, ad_groups, campaign_id=None):
        """Updates the specified ad groups in a campaign.

        https://msdn.microsoft.com/en-us/library/bing-ads-campaign-management-
        updateadgroups.aspx

        :type ad_groups: [_models.AdGroup]
        :param ad_groups:
          A list that can contain a maximum of 1,000 AdGroup objects to update.

        :type campaign_id: int
        :param campaign_id:
          The identifier of the campaign that owns the ad groups to update.
        """
        assert campaign_id
        for ad_group_chunk in _utils.chunked(
                ad_groups, chunk_size=self.predicate_list_limit):
            array_of_ad_group = _models.ArrayOfAdGroup(
                ad_groups=ad_group_chunk
            ).to_api_obj(self.campaign_service)
            self.campaign_service.UpdateAdGroups(
                AdGroups=array_of_ad_group, CampaignId=campaign_id
            )

    def get_ad_groups(self, campaign_ids=None):
        """Gets a list of AdGroup objects.

        :type campaign_ids: [int]
        :param campaign_ids:
          List of identifiers for the campaigns for which ad groups to get.

        :rtype: [_models.AdGroup]
        :return:
          Returned is a list of ad groups for the given campaign IDs.
        """
        if not campaign_ids:
            campaign_ids = [campaign.id for campaign in self.get_campaigns()]

        ad_groups = []
        for campaign_id in campaign_ids:
            ad_groups.extend(self.get_ad_groups_by_campaign_id(campaign_id))

        return ad_groups


    def get_ad_groups_by_status(self, status, campaign_ids=None):
        """Gets ad groups filtered on status.

        :type status: str
        :param status:
          Status of ad group, either `Active` or `Paused`.

        :type campaign_ids: [int] | None
        :param campaign_ids:
          List of campaign IDs to filter on.

        :rtype: [_models.AdGroup]
        :return:
          Returned is a list of ad groups filtered on status for the given
          campaign IDs.
        """
        _utils.validate_membership(status, _c.CAMPAIGN_STATUSES)
        ad_groups = self.get_ad_groups(campaign_ids=campaign_ids)
        return [
            ad_group for ad_group in ad_groups if ad_group.status == status
        ]

    def get_active_ad_groups(self):
        """Gets only active ad groups under active campaigns.

        :rtype: [_models.AdGroup]
        :return:
          Returned is a list of active ad groups.
        """
        campaigns = self.get_active_campaigns()
        active_campaign_ids = [campaign.id for campaign in campaigns]
        return self.get_ad_groups_by_status(_c.ACTIVE,
                                            campaign_ids=active_campaign_ids)

    def change_ad_groups_status(self, ad_group_ids, status):
        """Change the status of a list of ad groups.

        :type ad_group_ids: [int]
        :param ad_group_ids:
          List of identifiers for the ad groups for which to update statuses.

        :type status: str
        :param status:
          Status of ad group, either `Active` or `Paused`.
        """
        opposite_status = _c.ACTIVE if status == _c.PAUSED else _c.PAUSED
        ad_groups = [
            ad_group for ad_group in self.get_ad_groups_by_status(
                opposite_status
            ) if ad_group.id in ad_group_ids
        ]
        for ad_group in ad_groups:
            ad_group.status = status

        for campaign_id, campaign_ad_groups in (
                _it.groupby(ad_groups, _op.attrgetter('campaign_id'))):
            self.update_ad_groups(campaign_ad_groups, campaign_id=campaign_id)

    def pause_ad_groups(self, ad_group_ids):
        """Pauses ad groups in given account.

        :type ad_group_ids: [int]
        :param ad_group_ids:
          list of identifiers for the ad groups for which to update statuses.
        """
        self.change_ad_groups_status(ad_group_ids, _c.PAUSED)

    def activate_ad_groups(self, ad_group_ids):
        """Activates ad groups in given account.

        :type ad_group_ids: [int]
        :param ad_group_ids:
          list of identifiers for the ad groups for which to update statuses.
        """
        self.change_ad_groups_status(ad_group_ids, _c.ACTIVE)
