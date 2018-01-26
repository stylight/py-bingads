#!/usr/bin/env python
""" Base wrapper for all Bing Ads API operations. """
from __future__ import print_function
import functools as _ft
import logging as _logging

from bingads import authorization as _authorization
from bingads import service_client as _service_client
from bingads import exceptions as _bing_exc
from six import moves as _six_moves

from py_bingads import _constants as _c
from py_bingads import models as _models
from py_bingads import _utils

_logging.basicConfig(level=_logging.INFO)
# _logging.getLogger('suds.client').setLevel(_logging.INFO)
# _logging.getLogger('suds.transport.http').setLevel(_logging.INFO)
# _logging.getLogger('suds.client').setLevel(_logging.DEBUG)
# _logging.getLogger('suds.transport.http').setLevel(_logging.DEBUG)


class BingAds(object):
    """ A wrapper around the Bing Ads API. """

    VERSION = 11

    def __init__(self,  # pylint: disable=too-many-arguments
                 account_id=None, customer_id=None, developer_token=None,
                 environment=_c.PRODUCTION, client_id=None, client_state=None,
                 authentication_type=_c.OAUTH, username=None, password=None,
                 get_refresh_token=_utils.get_refresh_token,
                 save_refresh_token_callback=_utils.save_refresh_token,
                 predicate_list_limit=100):
        """
        :type account_id: int
        :param account_id:
          The identifier of the account that owns the entities in the request.
          Used as the CustomerAccountId header and the AccountId body elements
          in calls to the Bing Ads web services.

        :type customer_id: int
        :param customer_id:
          The identifier of the customer that owns the account.
          Used as the CustomerId header element in calls to the Bing Ads web
          services.

        :param developer_token: str
        :param developer_token:
          The Bing Ads developer access token.
          Used as the DeveloperToken header element in calls to the Bing Ads
          web services.

        :type environment: str
        :param environment:
          Represents which API environment to use, default is `production`,
          but `sandbox` can also be used for testing purposes.

        :type client_id: str
        :param client_id:
          The registered application's client ID.  Required for oauth.

        :param client_state: str | None
        :param client_state:
          Recommended for oauth. This is a non guessable 'state' request
          parameter to help prevent cross site request forgery (CSRF).

        :param authentication_type: str
        :param authentication_type:
          Type of authentication for Bing Ads service, either `oauth` or
          `username`. You should authenticate for Bing Ads production
          services with a Microsoft Account, instead of providing the Bing Ads
          username and password set. Authentication with a Microsoft
          Account is currently not supported in sandbox. Authentication with
          username and password credentials should only be used in sandbox.

        :type username: str | None
        :param username:
          The Bing Ads user's sign-in user name. Required for authentication
          with username.

        :type password: str | None
        :param password:
          The Bing Ads user's sign-in password.  Required for authentication
          with username.

        :type predicate_list_limit: int
        :param predicate_list_limit:
          Limits for number of items to send in service requests.
        """
        self._account_id = account_id  # Required?
        self.authorization_data = _authorization.AuthorizationData(
            account_id=account_id,
            customer_id=customer_id,
            developer_token=developer_token,
        )
        self.env = environment
        self._connected = False

        _utils.validate_membership(environment, _c.ENVIRONMENTS,
                                   name='environment')
        _utils.validate_membership(authentication_type,
                                   _c.AUTHENTICATION_TYPES,
                                   name='authentication_type')
        assert predicate_list_limit <= 100
        self.predicate_list_limit = predicate_list_limit

        if authentication_type == _c.USERNAME:
            assert environment == _c.SANDBOX, (
                'Authentication with username is only allowed in sandbox.'
            )
            self.connect_with_username(username, password)
        elif authentication_type == _c.OAUTH:
            assert environment == _c.PRODUCTION, (
                'Authentication with oauth is only allowed in production.'
            )
            self.connect_with_oauth(client_id, client_state, get_refresh_token,
                                    save_refresh_token_callback)

        self._services_cache = {}

    def connect_with_username(self, username, password):
        """ Connect using username and password. """
        assert username, (
            '`username` is required for authentication with username.'
        )
        assert password, (
            '`password` is required for authentication with username.'
        )
        assert not self._connected
        self.authorization_data.authentication = (
            _authorization.PasswordAuthentication(user_name=username,
                                                  password=password))
        self._connected = True

    def connect_with_oauth(self, client_id, client_state, get_refresh_token,
                           save_refresh_token_callback):
        """ Connect using OAuth. """
        assert client_id, (
            '`client_id` is required for authentication with oauth.'
        )
        if not client_state:
            _logging.warning(
                'Missing `client_state` which is recommended to help prevent '
                'cross site request forgery.'
            )

        authentication = _authorization.OAuthDesktopMobileAuthCodeGrant(
            client_id=client_id
        )
        authentication.state = client_state
        self.authorization_data.authentication = authentication

        self.authorization_data.authentication.token_refreshed_callback = \
            save_refresh_token_callback

        def request_user_consent():
            """ Request user content. """
            # TODO: Check whether using an interactive Python shell.
            print(authentication.get_authorization_endpoint())
            response_uri = _six_moves.input(
                'You need to provide consent for the application to access'
                ' your Bing Ads accounts. After you have granted consent '
                'in the web browser for the application to access your '
                'Bing Ads accounts, please enter the response URI that '
                'includes the authorization `code` parameter: \n >>>>> '
            )

            if authentication.state != client_state:
                raise Exception(
                    'The OAuth response state does not match the '
                    'client request state.'
                )

            # Request access and refresh tokens using the URI that you
            # provided manually during program execution.
            authentication.request_oauth_tokens_by_response_uri(
                response_uri=response_uri
            )

        refresh_token = get_refresh_token()

        # If we have a refresh token let's refresh it.
        if refresh_token:
            try:
                authentication.request_oauth_tokens_by_refresh_token(
                    refresh_token
                )
            except _bing_exc.OAuthTokenRequestException:
                request_user_consent()
        else:
            request_user_consent()

    def _get_service(self, name):
        """ Get a service by it's name. """
        if name not in self._services_cache:
            self._services_cache[name] = _service_client.ServiceClient(
                name,
                authorization_data=self.authorization_data,
                environment=self.env,
                version=self.VERSION,
            )
        return self._services_cache[name]

    def __getattr__(self, item):
        """Get a service; if service doesn't exit, raise AttributeError.

        :type item: str
        :param item:
          Attribute lookup name.

        :rtype: callable
        :return:
          If service name is recognized, return callable, else raise error.
        """
        service = item.split('get_')[-1]
        if service in _c.SERVICES:
            return _ft.partial(self._get_service, _c.SERVICES[service])
        raise AttributeError(
            '`BingAdsBase` has no attribute `{item}`.'.format(item=item)
        )

    @property
    def campaign_service(self):
        """ Get Campaign Management Service. """
        return self.get_campaign_service()

    def get_current_user_id(self):
        """ Get the user id for the currently logged in user of the API obj. """
        customer_service = self.get_customer_service()
        user = customer_service.GetUser(None)
        return user.User.Id

    def get_accounts_for_user_id(self, user_id=None):
        """Get accounts that this user has access to.

        :type user_id: int | None
        :param user_id:
          Optionally provide a user ID to get accounts.

        :rtype: [_models.Account]
        :return:
          Returned is a list of accounts for user.
        """
        customer_service = self.get_customer_service()
        if user_id is None:
            user_id = self.get_current_user_id()

        paging = dict(Index=0, Size=10)
        predicates = dict(Predicate=[
            dict(Field='UserId', Operator='Equals', Value=user_id)
        ])

        ret = []
        response = customer_service.SearchAccounts(
            PageInfo=paging, Predicates=predicates
        )
        while response:
            ret.extend(
                [_models.Account.from_api_obj(acc) for acc in response.Account]
            )
            paging['Index'] += 1
            response = customer_service.SearchAccounts(
                PageInfo=paging, Predicates=predicates
            )
        return ret

    @_utils.print_webfault
    def get_campaigns(self):
        """Get a list of campaigns.

        :rtype: [_models.Campaign]
        :return:
          List of `Campaign` objects.
        """
        campaign_service = self.get_campaign_service()

        response = campaign_service.GetCampaignsByAccountId(
            AccountId=self.authorization_data.account_id
        )
        return _models.ArrayOfCampaign.from_api_obj(response)

    @_utils.print_webfault
    def get_active_campaigns(self):
        """Get a list of active campaigns.

        :rtype: [_models.Campaign]
        :return:
          List of `Campaign` objects.
        """
        return [campaign for campaign in self.get_campaigns()
                if campaign.status == _c.ACTIVE]

    @_utils.print_webfault
    def get_paused_campaigns(self):
        """Get a list of paused campaigns.

        :rtype: [_models.Campaign]
        :return:
          List of `Campaign` objects.
        """
        return [campaign for campaign in self.get_campaigns()
                if campaign.status == _c.PAUSED]
