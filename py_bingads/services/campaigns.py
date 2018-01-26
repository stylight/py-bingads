#!/usr/bin/env python
""" Wrapper class for Campaigns. """
import logging as _logging

from py_bingads import _constants as _c
from py_bingads import _utils
from py_bingads import models as _models

from . import base as _base

_logging.basicConfig(level=_logging.INFO)


class Campaigns(_base.BingAds):
    """ Wrapper for Campaign service operations. """

    def __init__(self, **kwargs):
        """ Initialize Campaigns. """
        _base.BingAds.__init__(self, **kwargs)

    @_utils.print_webfault
    def update_campaigns(self, campaigns):
        """Updates specified campaigns in a specified account.

        :type campaigns: [_models.Campaign]
        :param campaigns:
          A list that contains Campaign objects to update.
        """
        for campaign_chunk in _utils.chunked(
                campaigns, chunk_size=self.predicate_list_limit):
            array_of_campaigns = _models.ArrayOfCampaign(
                campaigns=campaign_chunk
            ).to_api_obj(self.campaign_service)
            self.campaign_service.UpdateCampaigns(
                AccountId=self._account_id,
                Campaigns=array_of_campaigns,
            )

    def change_campaign_status(self, campaign_ids, status):
        """Change the status of a list of campaigns.

        :type campaign_ids: iter
        :param campaign_ids:
          Iterable of campaign IDs.

        :type status: str
          Status can be 'Active' or 'Paused'.
        """
        campaigns = [
            _models.Campaign(id=campaign_id, status=status) for
            campaign_id in campaign_ids
        ]
        self.update_campaigns(campaigns)

    def pause_campaigns(self, campaign_ids):
        """Pause campaigns with the given IDs.

        :type campaign_ids: iter
        :param campaign_ids:
          Iterable of campaign IDs.
        """
        self.change_campaign_status(campaign_ids, _c.PAUSED)

    def activate_campaigns(self, campaign_ids):
        """Activate campaigns with the given IDs.

        :type campaign_ids: iter
        :param campaign_ids:
          Iterable of campaign IDs.
        """
        self.change_campaign_status(campaign_ids, _c.ACTIVE)
