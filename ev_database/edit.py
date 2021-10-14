import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from electricvehicle import ElectricVehicle
from search import Search

JINJA_ENVIRNOMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Edit(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        key = self.request.get('key')
        newKey = ndb.Key(urlsafe=key)
        ev = newKey.get()


        template_values = {
                'user' : user,
                'ev' : ev,
                'key' : key,
        }

        template = JINJA_ENVIRNOMENT.get_template('edit.html')
        self.response.write(template.render(template_values))
