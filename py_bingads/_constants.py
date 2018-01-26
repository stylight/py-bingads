#!/usr/bin/env python
""" Bing API constant names """

# Environment types
PRODUCTION = 'production'
SANDBOX = 'sandbox'
ENVIRONMENTS = (PRODUCTION, SANDBOX)

# Authentication types
OAUTH = 'oauth'
USERNAME = 'username'
AUTHENTICATION_TYPES = (OAUTH, USERNAME)

# Campaign statuses
PAUSED = 'Paused'
ACTIVE = 'Active'
CAMPAIGN_STATUSES = (ACTIVE, PAUSED)

# Supported services
CUSTOMER_MANAGEMENT_SERVICE = 'CustomerManagementService'
CAMPAIGN_MANAGEMENT_SERVICE = 'CampaignManagementService'
SERVICES = dict(
    customer_service=CUSTOMER_MANAGEMENT_SERVICE,
    campaign_service=CAMPAIGN_MANAGEMENT_SERVICE,
)

# Association types
# https://msdn.microsoft.com/en-us/library/bing-ads-campaign-management-
# associationtype.aspx
ACCOUNT = 'Account'
CAMPAIGN = 'Campaign'
AD_GROUP = 'AdGroup'

ASSOCIATION_TYPES = (ACCOUNT, CAMPAIGN, AD_GROUP)

# DEVICES
DEVICE_PREFERENCE = 'DevicePreference'
ALL_DEVICES = 'all'
ALL_DEVICES_ID = 0
MOBILE = 'mobile'
MOBILE_ID = 30001

# Ad Extension Types
# https://msdn.microsoft.com/en-us/library/bing-ads-campaign-management-
# adextensionstypefilter.aspx
APP = 'AppAdExtension'
CALL = 'CallAdExtension'
CALLOUT = 'CalloutAdExtension'
IMAGE = 'ImageAdExtension'
LOCATION = 'LocationAdExtension'
REVIEW_AD = 'ReviewAdExtension'
SITELINK = 'Sitelink2AdExtension'
SITELINKS_DEPRECATED = 'SitelinksAdExtension'
STRUCTURED_SNIPPET = 'StructuredSnippetAdExtension'

AD_EXTENSION_TYPES = (
    APP, CALL, CALLOUT, IMAGE, LOCATION, REVIEW_AD, SITELINK,
    SITELINKS_DEPRECATED, STRUCTURED_SNIPPET,
)

# Shared Entity Types
NEGATIVE_KEYWORD = 'NegativeKeyword'
NEGATIVE_KEYWORD_LIST = 'NegativeKeywordList'
ARRAY_OF_SHARED_ENTITY = 'ArrayOfSharedEntity'
ARRAY_OF_SHARED_LIST_ITEM = 'ArrayOfSharedListItem'
SHARED_ENTITY_ASSOCITAION = 'SharedEntityAssociation'
ARRAY_OF_SHARED_ENTITY_ASSOCIATION = 'ArrayOfSharedEntityAssociation'

# Negative Keyword Match Typt
PHRASE = 'Phrase'
EXACT = 'Exact'
VALID_MATCH_TYPES = (PHRASE, EXACT)

# Ad Types
ALL_AD_TYPES = {
    'AdType': [
        'AppInstall',
        'DynamicSearch',
        'ExpandedText',
        'Image',
        'Product',
        'Text',
    ]
}
