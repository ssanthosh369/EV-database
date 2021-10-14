import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from electricvehicle import ElectricVehicle
from search import Search
from edit import Edit

JINJA_ENVIRNOMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Details(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()

        name = self.request.get('name')
        manu = self.request.get('manu')
        year = int(self.request.get('year'))



        query1 = ElectricVehicle.query(ElectricVehicle.name == name).fetch(keys_only=True)
        query2 = ElectricVehicle.query(ElectricVehicle.manufacturer == manu).fetch(keys_only=True)
        query3 = ElectricVehicle.query(ElectricVehicle.year == year).fetch(keys_only=True)

        total_query = ndb.get_multi(set(query1).intersection(query2).intersection(query3))

        avg = 0.0
        count = 0
        for i in total_query[0].reviews:
            avg += i.rating
            count += 1

        if count != 0:
            avg = avg / count

        template_values = {
            'user' : user,
            'total_query' : total_query[0],
            'length' : len(total_query),
            'key' : total_query[0].put().urlsafe(),
            'avg' : avg
        }

        template = JINJA_ENVIRNOMENT.get_template('details.html')
        self.response.write(template.render(template_values))



        # for i in query:
        #         self.response.write(i.name + "  " + i.manufacturer + "  " + str(i.year) + '<br/>')
