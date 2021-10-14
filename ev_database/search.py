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

class Search(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        if self.request.get('button') == 'Search':

            if not self.request.get('ev_name') and not self.request.get('ev_manufacturer') and not (self.request.get('ev_year_min')) and not (self.request.get('ev_year_max')) and not (self.request.get('ev_battery_size_min')) and not (self.request.get('ev_battery_size_max')) and not (self.request.get('ev_WLTP_range_min')) and not (self.request.get('ev_WLTP_range_max')) and not (self.request.get('ev_cost_min')) and not (self.request.get('ev_cost_max')) and not (self.request.get('ev_power_min')) and not (self.request.get('ev_power_max')):
                total_query = ElectricVehicle.query().fetch()

            else:
                if not (self.request.get('ev_name')):
                    query1 = ElectricVehicle.query().fetch(keys_only=True)
                else:
                    query1 = ElectricVehicle.query(ElectricVehicle.name == self.request.get('ev_name')).fetch(keys_only=True)

                if not (self.request.get('ev_manufacturer')):
                    query2 = ElectricVehicle.query().fetch(keys_only=True)
                else:
                    query2 = ElectricVehicle.query(ElectricVehicle.manufacturer == self.request.get('ev_manufacturer')).fetch(keys_only=True)

                if not (self.request.get('ev_year_min') and self.request.get('ev_year_max')):
                    query3 = ElectricVehicle.query().fetch(keys_only=True)
                else:
                    query3 = ElectricVehicle.query(ElectricVehicle.year >= int(self.request.get('ev_year_min')) , ElectricVehicle.year <= int(self.request.get('ev_year_max'))).fetch(keys_only=True)

                if not (self.request.get('ev_battery_size_min') and self.request.get('ev_battery_size_max')):
                    query4 = ElectricVehicle.query().fetch(keys_only=True)
                else:
                    query4 = ElectricVehicle.query(ElectricVehicle.battery_size >= float(self.request.get('ev_battery_size_min')) , ElectricVehicle.battery_size <= float(self.request.get('ev_battery_size_max'))).fetch(keys_only=True)

                if not (self.request.get('ev_WLTP_range_min') and self.request.get('ev_WLTP_range_max')):
                    query5 = ElectricVehicle.query().fetch(keys_only=True)
                else:
                    query5 = ElectricVehicle.query(ElectricVehicle.WLTP_range >= float(self.request.get('ev_WLTP_range_min')) , ElectricVehicle.WLTP_range <= float(self.request.get('ev_WLTP_range_max'))).fetch(keys_only=True)

                if not (self.request.get('ev_cost_min') and self.request.get('ev_cost_max')):
                    query6 = ElectricVehicle.query().fetch(keys_only=True)
                else:
                    query6 = ElectricVehicle.query(ElectricVehicle.cost >= float(self.request.get('ev_cost_min')) , ElectricVehicle.cost <= float(self.request.get('ev_cost_max'))).fetch(keys_only=True)

                if not (self.request.get('ev_power_min') and self.request.get('ev_power_max')):
                    query7 = ElectricVehicle.query().fetch(keys_only=True)
                else:
                    query7 = ElectricVehicle.query(ElectricVehicle.power >= float(self.request.get('ev_power_min')) , ElectricVehicle.power <= float(self.request.get('ev_power_max'))).fetch(keys_only=True)

                total_query = ndb.get_multi(set(query1).intersection(query2).intersection(query3).intersection(query4).intersection(query5).intersection(query6).intersection(query7))

            template_values = {
                    'total_query' : total_query,
                    'length' : len(total_query),
            }

            template = JINJA_ENVIRNOMENT.get_template('search.html')
            self.response.write(template.render(template_values))

            #self.redirect('/search')


        elif self.request.get('button') == 'Cancel':
                self.redirect('/')
