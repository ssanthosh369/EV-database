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

class CompareDetails(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        key = self.request.get('selected', allow_multiple=True)
        count = 0
        newKey = []
        for a in key:
            newKey.append(ndb.Key(urlsafe=a))

        ev = ndb.get_multi(newKey)
        avg = 0.0
        count = 0
        if len(newKey) != 0:
            for i in ev[0].reviews:
                avg += i.rating
                count += 1
            if count != 0:
                avg = avg / count

            minavg = maxavg = avg
            minyear = maxyear = ev[0].year
            minbat = maxbat = ev[0].battery_size
            minwltp = maxwltp = ev[0].WLTP_range
            mincost = maxcost = ev[0].cost
            minpower = maxpower = ev[0].power

        else:
            minavg = maxavg = avg
            minyear = maxyear = 0
            minbat = maxbat = 0
            minwltp = maxwltp = 0
            mincost = maxcost = 0
            minpower = maxpower = 0

        allAvg = []

        for i in ev:
            if minyear > i.year:
                minyear = i.year

            if maxyear < i.year:
                maxyear = i.year

            if minbat > i.battery_size:
                minbat = i.battery_size

            if maxbat < i.battery_size:
                maxbat = i.battery_size

            if minwltp > i.WLTP_range:
                minwltp = i.WLTP_range

            if maxwltp < i.WLTP_range:
                maxwltp = i.WLTP_range

            if mincost > i.cost:
                mincost = i.cost

            if maxcost < i.cost:
                maxcost = i.cost

            if minpower > i.power:
                minpower = i.power

            if maxpower < i.power:
                maxpower = i.power

            avg = 0.0
            count = 0
            for j in i.reviews:
                avg += j.rating
                count += 1
            if count != 0:
                avg = avg / count
            allAvg.append(avg)
            if minavg > avg:
                minavg = avg
            if maxavg < avg:
                maxavg = avg



        template_values = {
            'length' : len(newKey),
            'i' : ev,
            'key': key,
            'minyear' : minyear,
            'maxyear' : maxyear,
            'minbat' : minbat,
            'maxbat' : maxbat,
            'mincost' : mincost,
            'maxcost' : maxcost,
            'minwltp' : minwltp,
            'maxwltp' : maxwltp,
            'minpower' : minpower,
            'maxpower' : maxpower,
            'minavg' : minavg,
            'maxavg' : maxavg,
            'avg' : allAvg,
        }

        template = JINJA_ENVIRNOMENT.get_template('compareDetails.html')
        self.response.write(template.render(template_values))


        if self.request.get('button') == 'Cancel':
            self.redirect('/')


        # for i in query:
        #         self.response.write(i.name + "  " + i.manufacturer + "  " + str(i.year) + '<br/>')
