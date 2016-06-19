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


class ActivityMetaData(EndpointsModel):

    # groups of activities that can be reported together
    # content #community #techtalk #bugreport #forumpost #opensourcecode
    activity_group = ndb.StringProperty()

    # bugreport, techtalk, applies to all
    title = ndb.StringProperty()

    # applies to all, provides more detail / abstract about the activity
    description = ndb.StringProperty()

    # sub activity type
    type = ndb.StringProperty()

    # for all types, can be event link/blog link/github link/...
    link = ndb.StringProperty()

    # impact is about the number of people impacted
    # views for #blogpost, attendess for #techtalks ...
    impact = EndpointsVariantIntegerProperty(variant=messages.Variant.INT32)

    # for some acivities, links to slides, video's etc
    other_link1 = ndb.StringProperty()
    other_link2 = ndb.StringProperty()

    # community, techtalk
    location = ndb.StringProperty()
    google_expensed = ndb.BooleanProperty()
    us_approx_amount = EndpointsVariantIntegerProperty(
        variant=messages.Variant.INT32)


class ActivityRecord(EndpointsModel):

    _message_fields_schema = (
        'id',
        'gplus_id',
        'date',
        'title',
        'description',
        'location',
        'country',
        'activity_types',
        'activity_posts',
        'metric_reached',
        'metric_indirect',
        'metric_trained'
    )

    _api_key = None

    # MVP fields
    gplus_id = ndb.StringProperty()
    date = ndb.DateProperty()
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    location = ndb.StringProperty()
    country = ndb.StringProperty()
    activity_types = ndb.StringProperty(repeated=True)
    activity_posts = ndb.StringProperty(repeated=True)

    @EndpointsComputedProperty(property_type=messages.IntegerField, variant=messages.Variant.INT32)
    def metric_reached(self):
        # TODO: put some logic here
        return 0

    @EndpointsComputedProperty(property_type=messages.IntegerField, variant=messages.Variant.INT32)
    def metric_indirect(self):
        # TODO: put some logic here
        return 0

    @EndpointsComputedProperty(property_type=messages.IntegerField, variant=messages.Variant.INT32)
    def metric_trained(self):
        # TODO: put some logic here
        return 0

    def ApiKeySet(self, value):
        self._api_key = value

    @EndpointsAliasProperty(setter=ApiKeySet, property_type=messages.StringField)
    def api_key(self):
        return self._api_key

    def DummySetter(self, value):
        # do nothing since property will not be updated from API methods
        return

    @EndpointsAliasProperty(setter=DummySetter, property_type=messages.StringField)
    def gde_name(self):
        if self.gplus_id is None:
            return None
        gde = ndb.Key(Account, self.gplus_id).get()
        if gde is None:
            return None
        return gde.display_name

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
    # activity types and product groups
    product_groups = ndb.StringProperty(repeated=True)

    #  activity type metadata
    metadata = ndb.StructuredProperty(ActivityMetaData, repeated=True)

    deleted = ndb.BooleanProperty()