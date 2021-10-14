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

class Delete(webapp2.RequestHandler):
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
                'total_query' : ev,
        }

        if self.request.get('button') == 'Delete':
            ev.key.delete()




        template = JINJA_ENVIRNOMENT.get_template('delete.html')
        self.response.write(template.render(template_values))
