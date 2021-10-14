from google.appengine.ext import ndb

class Review(ndb.Model):
    review = ndb.StringProperty()
    rating = ndb.IntegerProperty()
