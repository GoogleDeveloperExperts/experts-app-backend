# gde-app-backend
Future home for the backend source of the Expert Tracking App

# Makefile for development / deployment
Please check Makefile for reference (Makefile can be frustrating to work with if you mix tab and spaces).

    $ make          # Run local dev server by default.

    $ make deploy        # Deploy the app depending on project and version in the Makefile.

    $ make dev           # Run local dev server

    $ make chrome_dev   # Start Chrome with unsafely-treat-insecure-origin-as-secure to test API locally.

## TODO
The key aspect of today is the need to product_group [repeated] in profiles and product_group in ActivityRecord.

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
    product_groups = ndb.StringProperty(repeated=True)
    
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
    product_groups = ndb.StringProperty(repeated=True)

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