# -*- coding: utf-8 -*-
""" Wrapper class for Sitelinks. """
import logging as _logging
import operator as _op

from py_bingads import _constants as _c
from py_bingads import _utils
from py_bingads import models as _models

from . import ad_extensions as _ad_extensions

_logging.basicConfig(level=_logging.INFO)


class Sitelinks(_ad_extensions.AdExtensions):
    """ Wrapper for Sitelinks service operations. """

    def __init__(self, check_sitelink_migration_status=True, **kwargs):
        """Initialize Sitelinks.

        :type check_sitelink_migration_status: bool
        :param check_sitelink_migration_status:
          Raise AssertionError on initialization if sitelink migration is
          not complete for account.
        """
        _ad_extensions.AdExtensions.__init__(self, **kwargs)

        if check_sitelink_migration_status:
            assert self.sitelink_migration_status()
        self.sitelink_ad_extension_type = _c.SITELINK
        self.ad_extension_class = _models.Sitelink2AdExtension

    def sitelink_migration_status(self):
        """To prepare for the sitelink ad extensions migration by the end
        of September 2017, you will need to determine whether the account has
        been migrated from SiteLinksAdExtension to Sitelink2AdExtension.
        All ad extension service operations available for both types of
        sitelinks; however you will need to determine which type to add,
        update, and retrieve.
        """
        sitelink_migration_is_completed = False
        sitelink_migration = 'SiteLinkAdExtension'
        customer_service = self.get_customer_service()

        # Optionally you can find out which pilot features the customer is
        # able to use. Even if the customer is in pilot for sitelink
        # migrations, the accounts that it contains might not be migrated.
        feature_pilot_flags = customer_service.GetCustomerPilotFeatures(
            self.authorization_data.customer_id
        )

        # The pilot flag value for Sitelink ad extension migration is 253.
        # Pilot flags apply to all accounts within a given customer; however,
        # each account goes through migration individually and has its own
        # migration status.
        if 253 in feature_pilot_flags['int']:
            # Account migration status below will be either NotStarted,
            # InProgress, or Completed.
            _logging.info('Customer is in pilot for Sitelink migration.')
        else:
            # Account migration status below will be NotInPilot.
            _logging.info('Customer is not in pilot for Sitelink migration.')

        # Even if you have multiple accounts per customer, each account will
        # have its own migration status. This checks one account using the
        # provided AuthorizationData.
        infos = self.campaign_service.GetAccountMigrationStatuses(dict(
            long=self.authorization_data.account_id
        ), sitelink_migration)

        for info in infos['AccountMigrationStatusesInfo']:
            _logging.info(info)
            for migration_status_info in info['MigrationStatusInfo']:
                migration_status = migration_status_info[1][0].Status
                migration_type = migration_status_info[1][0].MigrationType
                if migration_status == 'Completed' and (
                        sitelink_migration == migration_type):
                    sitelink_migration_is_completed = True

        return sitelink_migration_is_completed

    @_utils.print_webfault
    def delete_all_sitelinks(self):
        """Delete all sitelinks in the given account.

        https://msdn.microsoft.com/en-us/library/bing-ads-campaign-
        management-deleteadextensions.aspx
        """
        sitelink_ids = self.get_ad_extension_ids_by_account_id()
        _logging.info('Deleting %d sitelinks for account %d.',
                      len(sitelink_ids), self.authorization_data.account_id)
        self.delete_ad_extensions(sitelink_ids)

    @_utils.print_webfault
    def delete_campaign_sitelinks(self):
        """Delete all campaign-level associated sitelinks in the given
        account.

        https://msdn.microsoft.com/en-us/library/bing-ads-campaign-
        management-deleteadextensions.aspx
        """
        sitelink_ids = self.get_ad_extension_ids_by_account_id(
            association_type=_c.CAMPAIGN
        )
        _logging.info('Deleting %d campaign-level sitelinks for account %d.',
                      len(sitelink_ids), self.authorization_data.account_id)
        self.delete_ad_extensions(sitelink_ids)

    @_utils.print_webfault
    def get_all_sitelinks(self):
        """Get a list of all sitelinks in account's library.

        :rtype: [_models.Sitelink2AdExtension]
        :return:
          Returned is a list of sitelink ad extensions.
        """
        sitelink_ids = self.get_ad_extension_ids_by_account_id()
        return self.get_ad_extensions_by_ids(sitelink_ids)

    @_utils.print_webfault
    def get_campaign_sitelinks_grouped(self, campaign_ids=None):
        """Get a dict of campaign-id to list of sitelinks.

        :type campaign_ids: [int] | None
        :param campaign_ids:
          Iterable of campaign IDs. If not provided, all campaign IDs for
          account will be used.

        :rtype: dict
        :return:
          Returned is a dict keyed on Campaign IDs with values of the
          campaign's list of corresponding sitelinks.
        """
        if not campaign_ids:
            campaign_ids = [c.id for c in self.get_campaigns()]

        return self.get_ad_extensions_associations(
            association_type=_models.Campaign.TYPE_NAME,
            entity_ids=campaign_ids
        )

    @_utils.print_webfault
    def update_campaign_sitelinks(self, campaign_id, sitelinks):
        """Update set of campaign sitelinks.

        :type campaign_ids: int
        :param campaign_ids:
          Campaign identifier for which to update sitelinks.

        :type sitelinks: [_models.Sitelink2AdExtension]
        :param sitelinks:
          List of sitelink objects to create.
          Returned are the list of sitelink ad extensions.
        """
        if len(sitelinks) > 10:
            raise RuntimeError(
                'Cannot add more than 10 MAC sitelinks. '
                'Account Id: %d, Campaign Id: %d'
                % (self.authorization_data.account_id, campaign_id)
            )

        local_sitelinks = ((sitelink.key, sitelink) for sitelink in sorted(
            sitelinks, key=_op.attrgetter('key')
        ))
        remote_sitelinks = ((sitelink.key, sitelink) for sitelink in sorted(
            self.get_all_sitelinks(), key=_op.attrgetter('key')
        ))

        sitelinks_to_add = []
        sitelinks_to_update = []
        seen_keys = set()
        for key, (remote, local) in _utils.merge(
                remote_sitelinks, local_sitelinks):
            if key in seen_keys:
                raise ValueError('Duplicate key: %s' % key)
            if local is None:  # Keep in remote sitelink in library.
                continue
            if remote is None:  # Add local sitelink to library.
                sitelinks_to_add.append(local)
                seen_keys.add(key)
            elif remote != local:  # Update remote sitelink to local changes.
                local.id = remote.id
                sitelinks_to_update.append(local)
                seen_keys.add(key)

        # Add new local sitelinks to remote library.
        added_sitelink_ids = self.add_ad_extensions(
            _models.ArrayOfAdExtension(ad_extensions=sitelinks_to_add)
        )
        for id_, sitelink in zip(added_sitelink_ids, sitelinks_to_add):
            sitelink.id = id_.id

        self.update_ad_extensions(_models.ArrayOfAdExtension(
            ad_extensions=sitelinks_to_update
        ))
        self.associate_campaign_ad_extensions(
            [(campaign_id, sitelink.id) for sitelink
             in sitelinks_to_add + sitelinks_to_update]
        )
