import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from electricvehicle import ElectricVehicle

JINJA_ENVIRNOMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class AddConfirm(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()



    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        if self.request.get('button') == 'Add':
            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()


            ev = ElectricVehicle()
            ev.name = self.request.get('ev_name')
            ev.manufacturer = self.request.get('ev_manufacturer')
            ev.year = int(self.request.get('ev_year'))
            ev.battery_size = float(self.request.get('ev_battery_size'))
            ev.WLTP_range = float(self.request.get('ev_WLTP_range'))
            ev.cost = float(self.request.get('ev_cost'))
            ev.power = float(self.request.get('ev_power'))

            query1 = ElectricVehicle.query(ElectricVehicle.name == ev.name).fetch(keys_only=True)
            query2 = ElectricVehicle.query(ElectricVehicle.manufacturer == ev.manufacturer).fetch(keys_only=True)
            query3 = ElectricVehicle.query(ElectricVehicle.year == ev.year).fetch(keys_only=True)

            total_query = ndb.get_multi(set(query1).intersection(query2).intersection(query3))

            if len(total_query) == 0:
                ev.put()
                duplicate = False
            else:
                duplicate = True


        elif self.request.get('button') == 'Cancel':
            self.redirect('/')


        template_values = {
            'myuser' : myuser,
            'ev' : ev,
            'duplicate' : duplicate
        }

        template = JINJA_ENVIRNOMENT.get_template('addConfirm.html')
        self.response.write(template.render(template_values))
