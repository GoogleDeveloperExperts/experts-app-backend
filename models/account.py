from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb import EndpointsModel
from endpoints_proto_datastore.ndb import EndpointsAliasProperty
from protorpc import messages


class AccountGeoCode(EndpointsModel):
    lat = ndb.FloatProperty()
    lng = ndb.FloatProperty()


class Account(EndpointsModel):
    _message_fields_schema = (
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
        'product_group',
        'skills',
        'biography',
        'product_group'
    )

    _api_key = None

    # MVP fields
    display_name = ndb.StringProperty()
    email = ndb.StringProperty(required=True)
    type = ndb.StringProperty() # GDE type, read only field
    city = ndb.StringProperty()
    country = ndb.StringProperty()
    social_twitter = ndb.StringProperty()
    social_googleplus = ndb.StringProperty()
    social_facebook = ndb.StringProperty()
    social_stackoverflow = ndb.StringProperty()
    social_github = ndb.StringProperty()
    social_linkedin = ndb.StringProperty()
    social_website = ndb.StringProperty()
    pg_filename = ndb.StringProperty()
    pic_url = ndb.StringProperty()
    product_group = ndb.StringProperty(repeated=True)
    skills = ndb.StringProperty(repeated=True)
    biography = ndb.TextProperty()


    def ApiKeySet(self, value):
        self._api_key = value

    @EndpointsAliasProperty(setter=ApiKeySet, property_type=messages.StringField)
    def api_key(self):
        return self._api_key

    def IdSet(self, value):
        if not isinstance(value, basestring):
            raise TypeError('ID must be a string.')
        self.UpdateFromKey(ndb.Key(Account, value))

    @EndpointsAliasProperty(setter=IdSet, required=True)
    def id(self):
        if self.key is not None:
            return self.key.string_id()


    # fields below are not part of MVP and maybe removed
    gplus_id = ndb.StringProperty()
    gplus_page = ndb.StringProperty()
    real_name = ndb.StringProperty()
    auth_email = ndb.StringProperty()
    region = ndb.StringProperty()
    ctry_filename = ndb.StringProperty()
    geocode = ndb.StructuredProperty(AccountGeoCode)
    deleted = ndb.BooleanProperty()
    so_id = ndb.StringProperty()

