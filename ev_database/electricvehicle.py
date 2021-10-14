from google.appengine.ext import ndb
from review import Review

class ElectricVehicle(ndb.Model):
    # Attributes of the electric ElectricVehicle
    name = ndb.StringProperty()
    manufacturer = ndb.StringProperty()
    year = ndb.IntegerProperty()
    battery_size = ndb.FloatProperty()
    WLTP_range = ndb.FloatProperty()
    cost = ndb.FloatProperty()
    power = ndb.FloatProperty()
    reviews = ndb.StructuredProperty(Review, repeated=True)
