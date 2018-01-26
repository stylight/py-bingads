# -*- coding: utf-8 -*-
""" Wrapper class for Reviews. """
import logging as _logging
import operator as _op

from py_bingads import _constants as _c
from py_bingads import _utils
from py_bingads import models as _models

from . import ad_extensions as _ad_extensions

_logging.basicConfig(level=_logging.INFO)


class MaximumExtensionsExceeded(ValueError):
    """ The maximum number of accepted extensions has been exceeded """


class Reviews(_ad_extensions.AdExtensions):
    """ Wrapper for Reviews service operations. """

    def __init__(self, **kwargs):
        """ Initialize Reviews. """
        _ad_extensions.AdExtensions.__init__(self, **kwargs)
        self.ad_extension_class = _models.ReviewAdExtension

    def get_review_ids(self):
        """Get IDs of all reviews from account's review library.

        :rtype: [int]
        :return:
          Returns list of review IDs associated to campaigns for this account.
        """
        return self.get_ad_extension_ids_by_account_id(
            association_type=_c.CAMPAIGN
        )

    def get_reviews(self, review_ids=None):
        """Gets the specified reviews from the account's review library.

        :type review_ids: [int]
        :param review_ids:
          List of review IDs. If not provided, all reviews in account's
          review library associated to campaigns will be returned.

        :rtype: [_models.ReviewAdExtension]
        :return:
          Returned is a list of existing ReviewAdExtension objects.
        """
        if not review_ids:
            review_ids = self.get_review_ids()

        return self.get_ad_extensions_by_ids(review_ids)

    def get_review_associations(self, campaign_ids=None):
        """Gets the review associations for campaigns in account.

        :type campaign_ids: [int] | None
        :param campaign_ids:
          Iterable of campaign IDs. If not provided, all campaign IDs for
          account will be used.

        :rtype: dict
        :return:
          Returned is a dict keyed on a campaign ID with values as a list of
          corresponding reviews.
        """
        if not campaign_ids:
            campaign_ids = [c.id for c in self.get_campaigns()]

        return self.get_ad_extensions_associations(
            association_type=_models.Campaign.TYPE_NAME,
            entity_ids=campaign_ids
        )

    def update_reviews(self, reviews):
        """Updates reviews in account's library and associate to all campaigns.
        This operation creates new reviews, keeps reviews that exist and are
        in `reviews`, and deletes reviews that exist but are not in `reviews`.

        :type reviews: [_model.ReviewAdExtension]
        :param reviews:
          Reviews to update to account.
        """
        # FIXME: bing can do max 100, so why 20?
        if len(reviews) > 20:
            raise MaximumExtensionsExceeded(
                'Account: %s' % str(self.authorization_data.account_id))

        local_reviews = ((review.key, review) for review in sorted(
            reviews,
            key=_op.attrgetter('key')
        ))
        remote_reviews = ((review.key, review) for review in sorted(
            self.get_reviews(),
            key=_op.attrgetter('key')
        ))

        reviews_to_add = []
        reviews_to_keep = []
        review_ids_to_delete = []
        seen_keys = set()
        for key, (remote, local) in _utils.merge(
                remote_reviews, local_reviews):
            if local is None:  # Delete in remote review in library.
                review_ids_to_delete.append(remote.id)
            elif remote is None:  # Add local review to library.
                if local.key not in seen_keys:  # If not there already.
                    reviews_to_add.append(local)
                    seen_keys.add(key)
            else:
                reviews_to_keep.append(remote)
                seen_keys.add(key)

        # Delete first to make room for the new. Bing also deletes campaign
        # associations along with the object.
        self.delete_ad_extensions(review_ids_to_delete)

        # Create new reviews.
        added_review_ids = self.add_ad_extensions(
            _models.ArrayOfAdExtension(ad_extensions=reviews_to_add)
        )
        for id_, review in zip(added_review_ids, reviews_to_add):
            review.id = id_.id

        # Associate new and existing reviews.
        campaign_ids = [c.id for c in self.get_campaigns()]
        self.associate_campaign_ad_extensions([
            (campaign_id, review.id)
            for campaign_id in campaign_ids
            for review in reviews_to_add + reviews_to_keep
        ])
