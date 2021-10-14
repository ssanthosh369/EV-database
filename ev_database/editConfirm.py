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

class EditConfirm(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        key = self.request.get('key')
        newKey = ndb.Key(urlsafe=key)
        ev = newKey.get()
        copy = ev
        dup = False

        if self.request.get('button') == 'Confirm':
            name = ev.name
            manu = ev.manufacturer
            year = ev.year
            bat = ev.battery_size
            wltp = ev.WLTP_range
            cost = ev.cost
            power = ev.power

            ev.name = self.request.get('ev_name')
            ev.manufacturer = self.request.get('ev_manufacturer')
            ev.year = int(self.request.get('ev_year'))
            ev.battery_size = float(self.request.get('ev_battery_size'))
            ev.WLTP_range = float(self.request.get('ev_WLTP_range'))
            ev.cost = float(self.request.get('ev_cost'))
            ev.power = float(self.request.get('ev_power'))
            if(name != ev.name or manu != ev.manufacturer or year != ev.year):
                query1 = ElectricVehicle.query(ElectricVehicle.name == ev.name).fetch(keys_only=True)
                query2 = ElectricVehicle.query(ElectricVehicle.manufacturer == ev.manufacturer).fetch(keys_only=True)
                query3 = ElectricVehicle.query(ElectricVehicle.year == ev.year).fetch(keys_only=True)
                total_query = ndb.get_multi(set(query1).intersection(query2).intersection(query3))
                if(len(total_query) > 0):
                    dup = True

            if(dup == False):
                ev.put()


        elif self.request.get('button') == 'Cancel':
            self.redirect('/')


        template_values = {
                'user' : user,
                'ev' : ev,
                'key' : newKey,
                'name' : name,
                'manufacturer' : manu,
                'year' : year,
                'battery_size' : bat,
                'WLTP_range' : wltp,
                'cost' : cost,
                'power' : power,
                'dup' : dup
        }

        template = JINJA_ENVIRNOMENT.get_template('editConfirm.html')
        self.response.write(template.render(template_values))
