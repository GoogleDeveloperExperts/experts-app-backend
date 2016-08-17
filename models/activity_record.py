from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb import EndpointsModel
from endpoints_proto_datastore.ndb import EndpointsAliasProperty
from endpoints_proto_datastore.ndb import EndpointsVariantIntegerProperty
from endpoints_proto_datastore.ndb import EndpointsComputedProperty
from datetime import datetime
from protorpc import messages

from models.activity_post import ActivityPost
from models.account import Account

import logging

import math


class ActivityRecord(EndpointsModel):

    _message_fields_schema = (
        'id',
        'email',
        'date',
        'title',
        'description',
        'city',
        'country',
        'activity_types',
        'activity_posts',
        'metric_reached',
        'metric_indirect',
        'metric_trained',
        'product_groups'
    )

    _api_key = None

    # MVP fields
    email = ndb.StringProperty(required=True)
    date = ndb.DateProperty()
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    city = ndb.StringProperty()
    country = ndb.StringProperty()
    activity_types = ndb.StringProperty(repeated=True)
    activity_posts = ndb.StringProperty(repeated=True)
    product_groups = ndb.StringProperty(repeated=True)

    @EndpointsComputedProperty(property_type=messages.IntegerField, variant=messages.Variant.INT32)
    def metric_reached(self):
        total_reached = 0

        if len(self.activity_posts) == 0:
            return total_reached

        for post_id in self.activity_posts:
            post_key = ndb.Key(ActivityPost, int(post_id))
            logging.info(post_key)
            activity_post = post_key.get()
            total_reached += activity_post.metric_reached
        return total_reached

    @EndpointsComputedProperty(property_type=messages.IntegerField, variant=messages.Variant.INT32)
    def metric_indirect(self):
        total_indirect = 0

        if len(self.activity_posts) == 0:
            return total_indirect

        for post_id in self.activity_posts:
            post_key = ndb.Key(ActivityPost, int(post_id))
            logging.info(post_key)
            activity_post = post_key.get()
            total_indirect += activity_post.metric_indirect
        return total_indirect

    @EndpointsComputedProperty(property_type=messages.IntegerField, variant=messages.Variant.INT32)
    def metric_trained(self):
        total_trained = 0

        if len(self.activity_posts) == 0:
            return total_trained

        for post_id in self.activity_posts:
            post_key = ndb.Key(ActivityPost, int(post_id))
            logging.info(post_key)
            activity_post = post_key.get()
            total_trained += activity_post.metric_trained
        return total_trained

    def ApiKeySet(self, value):
        self._api_key = value

    @EndpointsAliasProperty(setter=ApiKeySet, property_type=messages.StringField)
    def api_key(self):
        return self._api_key

    # def DummySetter(self, value):
    #     # do nothing since property will not be updated from API methods
    #     return

    # @EndpointsAliasProperty(setter=DummySetter, property_type=messages.StringField)
    # def gde_name(self):
    #     if self.gplus_id is None:
    #         return None
    #     gde = ndb.Key(Account, self.gplus_id).get()
    #     if gde is None:
    #         return None
    #     return gde.display_name

    # fields below are not part of MVP and maybe removed

    # dates: are they really useful????
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    date_updated = ndb.DateTimeProperty(auto_now=True)
    # first post date, will be more interesting
    post_date = ndb.StringProperty()
    # related posts, we store the post_id's and the activity link
    # in some case the activity link is the gplus_post link itself
    # when there are no links attached to the post
    activity_link = ndb.StringProperty()
    activity_title = ndb.StringProperty()
    gplus_posts = ndb.StringProperty(repeated=True)
    # cumulative plus_oners & resharers
    plus_oners = EndpointsVariantIntegerProperty(
        variant=messages.Variant.INT32)
    resharers = EndpointsVariantIntegerProperty(variant=messages.Variant.INT32)
    comments = EndpointsVariantIntegerProperty(variant=messages.Variant.INT32)

    # #  activity type metadata
    # metadata = ndb.StructuredProperty(ActivityMetaData, repeated=True)

    deleted = ndb.BooleanProperty()