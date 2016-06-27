# gde-app-backend
Future home for the backend source of the Expert Tracking App

## Account
    display_name = ndb.StringProperty()
    email = ndb.StringProperty()
    type = ndb.StringProperty() # GDE type, read only field
    city = ndb.StringProperty()
    country = ndb.StringProperty()
    social_twitter = ndb.StringProperty()
    social_googleplus = ndb.StringProperty()
    social_facebook = ndb.StringProperty()
    social_stackoverflow = ndb.StringProperty()
    pg_filename = ndb.StringProperty()
    pic_url = ndb.StringProperty()
###### Field renames:
    location -> city
    ctry_filename -> country
    gplus_id -> social_googleplus
    so_id -> social_stackoverflow
###### Do we need it ? What is required on the frontend ?
    geocode
###### Field removed:
    product_group
    deleted


## Activity Record (Master Record)
    gplus_id = ndb.StringProperty()
    date = ndb.DateProperty()
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    city = ndb.StringProperty()
    country = ndb.StringProperty()
    activity_types = ndb.StringProperty(repeated=True)
    activity_posts = ndb.StringProperty(repeated=True)
    metric_reached = ndb.IntegerProperty()
    metric_indirect = ndb.IntegerProperty()
    metric_trained = ndb.IntegerProperty()

## Activity Post (Child Record)
    gplus_id = ndb.StringProperty()
    type = ndb.StringProperty()
    url = ndb.StringProperty()
    metric_reached = ndb.IntegerProperty()
    metric_indirect = ndb.IntegerProperty()
    metric_trained = ndb.IntegerProperty()

## Activity Group
    description = ndb.StringProperty()
    google_expensed = ndb.StringProperty()
    impact = ndb.StringProperty()
    link = ndb.StringProperty()
    city = ndb.StringProperty()
    other_link1 = ndb.StringProperty()
    other_link2 = ndb.StringProperty()
    tag = ndb.StringProperty()
    title = ndb.StringProperty()
    types = ndb.StringProperty(repeated=True)
    us_approx_amount = ndb.StringProperty()


## Activity Type
    description = ndb.StringProperty()
    group = ndb.StringProperty()
    tag = ndb.StringProperty()

## Product Group
    tag = ndb.StringProperty()
    category = ndb.StringProperty()
    description = ndb.StringProperty()
    image = ndb.StringProperty()
    product = ndb.StringProperty()
    so_tags = ndb.StringProperty(repeated=True)
    url = ndb.StringProperty()