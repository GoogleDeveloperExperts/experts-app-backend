import endpoints
from protorpc import remote
from models import ActivityDetail
from models import ActivityMaster
from models import Account
from models import ActivityType
from models import ProductGroup
from models import ActivityGroup

from google.appengine.ext import ndb

from .utils import check_auth

import logging


_CLIENT_IDs = [
    endpoints.API_EXPLORER_CLIENT_ID,
    '47242318878-dik3r14d8jc528h1ao35f8ehqa7tmpe1.apps.googleusercontent.com',
    '622745668355-rpeo1i7hjo4vj003dithtp1d71iniqqc.apps.googleusercontent.com',
    '66416776373-3k5goi8hn9d5rih68t8km57iliithohb.apps.googleusercontent.com'
]

api_root = endpoints.api(name='expertstracking', version='v2.0', allowed_client_ids=_CLIENT_IDs)


@api_root.api_class(resource_name='activity_master', path='activityMaster')
class ActivityMasterService(remote.Service):
    @ActivityMaster.method(request_fields=('id',), path='/activityMaster/{id}',
                           http_method='GET', name='get')
    def get(self, activity_master):
        if not activity_master.from_datastore:
            raise endpoints.NotFoundException('ActivityMaster not found.')
        return activity_master

    @ActivityMaster.method(path='/activityMaster', http_method='POST',
                           name='insert')
    def ActivityMasterInsert(self, activity_master):

        if not check_auth(activity_master.email, activity_master.api_key):
            raise endpoints.UnauthorizedException(
                'Only Experts and admins may enter or change data.')

        activity_master.put()
        return activity_master

    @ActivityMaster.method(path='/activityMaster/{id}', http_method='PUT',
                           name='update')
    def ActivityMasterUpdate(self, activity_master):
        if not activity_master.from_datastore:
            raise endpoints.NotFoundException('ActivityMaster not found.')

        if not check_auth(activity_master.email, activity_master.api_key):
            raise endpoints.UnauthorizedException(
                'Only Experts and admins may enter or change data.')

        activity_master.put()
        return activity_master

    @ActivityMaster.method(request_fields=('id', 'api_key',), response_fields=('id',),
                           path='/activityMaster/delete/{id}',
                           http_method='DELETE', name='delete')
    def ActivityMasterDelete(self, activity_master):
        if not activity_master.from_datastore:
            raise endpoints.NotFoundException('ActivityMaster not found.')

        if not check_auth(activity_master.email, activity_master.api_key):
            raise endpoints.UnauthorizedException(
                'Only Experts and admins may enter or change data.')

        # Mark associated Activity Details as deleted
        if activity_master.activity_details is not None and len(activity_master.activity_details) > 0:
            keys = [ndb.Key(ActivityDetail, int(id)) for id in activity_master.activity_details]
            activity_details = ndb.get_multi(keys)
            for activity_detail in activity_details:
                activity_detail.key.delete()

        activity_master.key.delete()
        return activity_master

    @ActivityMaster.query_method(query_fields=('limit', 'order', 'pageToken', 'email'),
                                 path='activityMaster', name='list')
    def ActivityMasterList(self, query):
        return query


@api_root.api_class(resource_name='activity_detail', path='activityDetail')
class ActivityDetailService(remote.Service):
    @ActivityDetail.method(request_fields=('id',), path='/activityDetail/{id}',
                         http_method='GET', name='get')
    def get(self, activity_detail):
        if not activity_detail.from_datastore:
            raise endpoints.NotFoundException('ActivityDetail not found.')
        return activity_detail

    @ActivityDetail.method(path='/activityDetail', http_method='POST',
                         name='insert')
    def ActivityDetailInsert(self, activity_detail):

        if not check_auth(activity_detail.email, activity_detail.api_key):
            raise endpoints.UnauthorizedException(
                'Only Experts and admins may enter or change data.')

        activity_detail.put()
        return activity_detail

    @ActivityDetail.method(path='/activityDetail/{id}', http_method='PUT',
                         name='update')
    def ActivityDetailUpdate(self, activity_detail):
        if not activity_detail.from_datastore:
            raise endpoints.NotFoundException('ActivityDetail not found.')

        if not check_auth(activity_detail.email, activity_detail.api_key):
            raise endpoints.UnauthorizedException(
                'Only Experts and admins may enter or change data.')

        activity_detail.put()
        return activity_detail

    @ActivityDetail.method(request_fields=('id', 'api_key',), response_fields=('id',),
                         path='/activityDetail/delete/{id}',
                         http_method='DELETE', name='delete')
    def ActivityDetailDelete(self, activity_detail):
        if not activity_detail.from_datastore:
            raise endpoints.NotFoundException('ActivityDetail not found.')

        if not check_auth(activity_detail.email, activity_detail.api_key):
            raise endpoints.UnauthorizedException(
                'Only Experts and admins may enter or change data.')

        #delete reference to AP in associated AR
        if activity_detail.activity_master is not None:
            ar_key = ndb.Key(ActivityMaster, int(activity_detail.activity_master))
            ar = ar_key.get()
            if ar is None:
                raise endpoints.NotFoundException('ActivityMaster not found.')
            logging.info(activity_detail.id)
            logging.info(ar.activity_details)
            if str(activity_detail.id) in ar.activity_details:
                ar.activity_details.remove(str(activity_detail.id))
                logging.info(ar.activity_details)
                ar.put()

        activity_detail.key.delete()
        return activity_detail

    @ActivityDetail.query_method(query_fields=('limit', 'order', 'pageToken', 'activity_master'),
                               path='activityDetail', name='list')
    def ActivityDetailList(self, query):
        return query


@api_root.api_class(resource_name='account', path='account')
class AccountService(remote.Service):
    @Account.method(path='/account/{id}', http_method='POST', name='insert',
                    request_fields=(
                            'api_key',
                            'id',
                            'display_name',
                            'email',
                            'type',
                            'city',
                            'country',
                            'social_twitter',
                            'social_googleplus',
                            'social_facebook',
                            'social_stackoverflow',
                            'social_github',
                            'social_linkedin',
                            'social_website',
                            'pg_filename',
                            'pic_url',
                            'deleted',
                            'skills',
                            'biography',
                            'product_group'
                    ),
                    response_fields=(
                            'id',
                            'display_name',
                            'email',
                            'type',
                            'city',
                            'country',
                            'social_twitter',
                            'social_googleplus',
                            'social_facebook',
                            'social_stackoverflow',
                            'social_github',
                            'social_linkedin',
                            'social_website',
                            'pg_filename',
                            'pic_url',
                            'deleted',
                            'skills',
                            'biography',
                            'product_group'
                    ))
    def AccountInsert(self, account):
        if not check_auth(account.email, account.api_key):
            raise endpoints.UnauthorizedException(
                'Only Admins may enter or change this data.')
        account.put()
        return account

    @Account.method(request_fields=('id',), path='/account/{id}',
                    http_method='GET', name='get')
    def get(self, account):
        if not account.from_datastore:
            raise endpoints.NotFoundException('Account not found.')
        return account

    @Account.query_method(query_fields=('limit', 'order', 'pageToken', 'type'),
                          path='account', name='list')
    def AccountList(self, query):
        return query


@api_root.api_class(resource_name='activity_type', path='activityType')
class ActivityTypeService(remote.Service):
    @ActivityType.method(path='/activityType/{id}', http_method='POST', name='insert',
                         request_fields=('id', 'tag', 'description', 'group', 'api_key'))
    def at_insert(self, activity_type):
        if not check_auth(None, activity_type.api_key):
            raise endpoints.UnauthorizedException(
                'Only Admins may enter or change this data.')

        activity_type.put()
        return activity_type

    @ActivityType.method(request_fields=('id',), path='/activityType/{id}',
                         http_method='GET', name='get')
    def at_get(self, activity_type):
        if not activity_type.from_datastore:
            raise endpoints.NotFoundException('Activity type not found.')
        return activity_type

    @ActivityType.method(request_fields=('id', 'api_key'), response_fields=("id",),
                         path='/activityType/{id}',
                         http_method='DELETE', name='delete')
    def at_delete(self, activity_type):
        if not activity_type.from_datastore:
            raise endpoints.NotFoundException('Activity type not found.')
        if not check_auth(None, activity_type.api_key):
            raise endpoints.UnauthorizedException(
                'Only Admins may enter or change this data.')

        activity_type.key.delete()

        return activity_type

    @ActivityType.query_method(query_fields=('limit', 'order', 'pageToken'),
                               path='/activityType', name='list')
    def at_list(self, query):
        return query


@api_root.api_class(resource_name='activity_group', path='activityGroup')
class ActivityGroupService(remote.Service):
    @ActivityGroup.method(path='/activityGroup/{id}', http_method='POST', name='insert',
                          request_fields=('id', 'tag', 'types', 'title', 'description', 'link',
                                          'impact', 'other_link1', 'other_link2', 'city',
                                          'google_expensed', 'us_approx_amount', 'api_key'))
    def ag_insert(self, activity_group):
        if not check_auth(None, activity_group.api_key):
            raise endpoints.UnauthorizedException(
                'Only Admins may enter or change this data.')

        activity_group.put()
        return activity_group

    @ActivityGroup.method(request_fields=('id',), path='/activityGroup/{id}',
                          http_method='GET', name='get')
    def ag_get(self, activity_group):
        if not activity_group.from_datastore:
            raise endpoints.NotFoundException('Activity type not found.')
        return activity_group

    @ActivityGroup.method(request_fields=('id', 'api_key'), response_fields=("id",),
                          path='/activityGroup/{id}',
                          http_method='DELETE', name='delete')
    def ag_delete(self, activity_group):
        if not activity_group.from_datastore:
            raise endpoints.NotFoundException('Activity type not found.')
        if not check_auth(None, activity_group.api_key):
            raise endpoints.UnauthorizedException(
                'Only Admins may enter or change this data.')

        activity_group.key.delete()

        return activity_group

    @ActivityGroup.query_method(query_fields=('limit', 'order', 'pageToken'),
                                path='/activityGroup', name='list')
    def ag_list(self, query):
        return query


@api_root.api_class(resource_name='product_group', path='productGroup')
class ProductGroupService(remote.Service):
    @ProductGroup.method(path='/productGroup/{id}', http_method='POST', name='insert',
                         request_fields=(
                                 'id', 'tag', 'description', 'category', 'product', 'url', 'image', 'api_key',
                                 'so_tags'))
    def pg_insert(self, product_group):
        if not check_auth(None, product_group.api_key):
            raise endpoints.UnauthorizedException(
                'Only Admins may enter or change this data.')

        product_group.put()
        return product_group

    @ProductGroup.method(request_fields=('id',), path='/productGroup/{id}',
                         http_method='GET', name='get')
    def pg_get(self, product_group):
        if not product_group.from_datastore:
            raise endpoints.NotFoundException('Activity type not found.')
        return product_group

    @ProductGroup.method(request_fields=('id', 'api_key'), response_fields=("id",),
                         path='/productGroup/{id}',
                         http_method='DELETE', name='delete')
    def pg_delete(self, product_group):
        if not product_group.from_datastore:
            raise endpoints.NotFoundException('Activity type not found.')
        if not check_auth(None, product_group.api_key):
            raise endpoints.UnauthorizedException(
                'Only Admins may enter or change this data.')

        product_group.key.delete()

        return product_group

    @ProductGroup.query_method(query_fields=('limit', 'order', 'pageToken'),
                               path='/productGroup', name='list')
    def pg_list(self, query):
        return query
