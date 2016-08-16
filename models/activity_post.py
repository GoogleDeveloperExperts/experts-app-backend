import re
import logging
from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb import EndpointsModel, EndpointsComputedProperty
from endpoints_proto_datastore.ndb import EndpointsAliasProperty
from endpoints_proto_datastore.ndb import EndpointsVariantIntegerProperty
from protorpc import messages
from models.activity_type import ActivityType
from models.product_group import ProductGroup


class ActivityPost(EndpointsModel):

    _message_fields_schema = (
        'id',
        'email',
        'type',
        'url',
        'metric_reached',
        'metric_indirect',
        'metric_trained',
        'activity_record'
    )

    _api_key = None

    # MVP fields
    email = ndb.StringProperty(required=True)
    type = ndb.StringProperty()
    url = ndb.StringProperty()
    metric_reached = ndb.IntegerProperty()
    metric_indirect = ndb.IntegerProperty()
    metric_trained = ndb.IntegerProperty()

    activity_record = ndb.StringProperty()

    def ApiKeySet(self, value):
        self._api_key = value

    @EndpointsAliasProperty(setter=ApiKeySet, property_type=messages.StringField)
    def api_key(self):
        return self._api_key



    # in the previous version the activity post as equal the the G+ post it
    # this is why we were setting it. This is no longer necessary. 
    #
    # def IdSet(self, value):
    #     if not isinstance(value, basestring):
    #         raise TypeError('ID must be a string.')
    #     self.UpdateFromKey(ndb.Key(ActivityPost, value))

    # @EndpointsAliasProperty(setter=IdSet, required=True)
    # def id(self):
    #     if self.key is not None:
    #         return self.key.string_id()

    # fields below are not part of MVP and maybe removed

    # tempted to use the G+ unique activity id ( stack overflow ?)
    post_id = ndb.StringProperty()
    # we identify Expert's uniquely using this
    gplus_id = ndb.StringProperty()
    name = ndb.StringProperty()
    # date at which the activity (post) was made
    date = ndb.StringProperty()
    plus_oners = EndpointsVariantIntegerProperty(
        variant=messages.Variant.INT32)
    resharers = EndpointsVariantIntegerProperty(variant=messages.Variant.INT32)
    comments = EndpointsVariantIntegerProperty(variant=messages.Variant.INT32)
    title = ndb.StringProperty()
    # url of the post (question for stack overflow)
    url = ndb.StringProperty()
    product_group = ndb.StringProperty(repeated=True)
    activity_type = ndb.StringProperty(repeated=True)
    links = ndb.StringProperty()

    deleted = ndb.BooleanProperty(default=False)