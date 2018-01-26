# -*- coding: utf-8 -*-
""" Wrapper class for Callouts. """
import logging as _logging
import operator as _op

from py_bingads import _constants as _c
from py_bingads import _utils
from py_bingads import models as _models

from . import ad_extensions as _ad_extensions

_logging.basicConfig(level=_logging.INFO)


class MaximumExtensionsExceeded(ValueError):
    """ The maximum number of accepted extensions has been exceeded """


class Callouts(_ad_extensions.AdExtensions):
    """ Wrapper for Callouts service operations. """

    def __init__(self, **kwargs):
        """ Initialize Callouts. """
        _ad_extensions.AdExtensions.__init__(self, **kwargs)
        self.ad_extension_class = _models.CalloutAdExtension

    def get_callout_ids(self):
        """Get IDs of all callouts from account's callout library.

        :rtype: [int]
        :return:
          Returns list of callout IDs associated to campaigns for this account.
        """
        return self.get_ad_extension_ids_by_account_id(
            association_type=_c.CAMPAIGN
        )

    def get_callouts(self, callout_ids=None):
        """Gets the specified callouts from the account's callout library.

        :type callout_ids: [int] | None
        :param callout_ids:
          List of callout IDs. If not provided, all callouts in account's
          callout library associated to campaigns will be returned.

        :rtype: [_models.CalloutAdExtension]
        :return:
          Returned is a list of existing CalloutAdExtension objects.
        """
        if not callout_ids:
            callout_ids = self.get_callout_ids()

        return self.get_ad_extensions_by_ids(callout_ids)

    def get_callout_associations(self, campaign_ids=None):
        """Gets the callout associations for campaigns in account.

        :type campaign_ids: [int] | None
        :param campaign_ids:
          Iterable of campaign IDs. If not provided, all campaign IDs for
          account will be used.

        :rtype: dict
        :return:
          Returned is a dict keyed on a campaign ID with values as a list of
          corresponding callouts.
        """
        if not campaign_ids:
            campaign_ids = [c.id for c in self.get_campaigns()]

        return self.get_ad_extensions_associations(
            association_type=_models.Campaign.TYPE_NAME,
            entity_ids=campaign_ids
        )

    def update_callouts(self, callouts):
        """Updates callouts in account's library and associate to all campaigns.
        This operation creates new callouts, keeps callouts that exist and are
        in `callouts`, and deletes callouts that exist but are not in
        `callouts`.

        :type callouts: [_model.CalloutAdExtension]
        :param callouts:
          Callouts to update to account.
        """
        # FIXME: bing can do max 100, so why 20?
        if len(callouts) > 20:
            raise MaximumExtensionsExceeded(
                'Account: %s' % str(self.authorization_data.account_id))

        local_callouts = ((callout.key, callout) for callout in sorted(
            callouts,
            key=_op.attrgetter('key')
        ))
        remote_callouts = ((callout.key, callout) for callout in sorted(
            self.get_callouts(),
            key=_op.attrgetter('key')
        ))

        callouts_to_add = []
        callouts_to_keep = []
        callout_ids_to_delete = []
        seen_keys = set()
        for key, (remote, local) in _utils.merge(
                remote_callouts, local_callouts):
            if local is None:  # Delete in remote callout in library.
                callout_ids_to_delete.append(remote.id)
            elif remote is None:  # Add local callout to library.
                if local.key not in seen_keys:  # If not there already.
                    callouts_to_add.append(local)
                    seen_keys.add(key)
            else:
                callouts_to_keep.append(remote)
                seen_keys.add(key)

        # Delete first to make room for the new. Bing also deletes campaign
        # associations along with the object.
        self.delete_ad_extensions(callout_ids_to_delete)

        # Create new callouts.
        added_callout_ids = self.add_ad_extensions(
            _models.ArrayOfAdExtension(ad_extensions=callouts_to_add)
        )
        for id_, callout in zip(added_callout_ids, callouts_to_add):
            callout.id = id_.id

        # Associate new and existing callouts.
        campaign_ids = [c.id for c in self.get_campaigns()]
        self.associate_campaign_ad_extensions([
            (campaign_id, callout.id)
            for campaign_id in campaign_ids
            for callout in callouts_to_add + callouts_to_keep
        ])
