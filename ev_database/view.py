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

class View(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        ev = ElectricVehicle()

        template_values = {
            'ev' : ev,
        }

        template = JINJA_ENVIRNOMENT.get_template('view.html')
        self.response.write(template.render(template_values))



        # for i in query:
        #         self.response.write(i.name + "  " + i.manufacturer + "  " + str(i.year) + '<br/>')
