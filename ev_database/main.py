# Assignment by: Santhosh Shanmugam
# Student no: 2976813
# Module : CPA assignment 1

import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from electricvehicle import ElectricVehicle
from myuser import MyUser
from add import Add
from view import View
from search import Search
from details import Details
from edit import Edit
from editConfirm import EditConfirm
from compare import Compare
from delete import Delete
from compareDetails import CompareDetails
from addReview import AddReview
from confirmReview import ConfirmReview
from addConfirm import AddConfirm

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        url_string = ''
        welcome = 'Welcome back,'

        user = users.get_current_user()

        if user:
            url= users.create_logout_url(self.request.uri)
            url_string = 'Logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                welcome = 'Welcome new user,'
                myuser = MyUser(id=user.user_id())
                myuser.put()

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'Login'

        template_values = {
                    'url' : url,
                    'url_string' : url_string,
                    'user' : user,
                    'welcome' : welcome
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
            ('/',MainPage),
            ('/add', Add),
            ('/addConfirm', AddConfirm),
            ('/view', View),
            ('/search', Search),
            ('/details', Details),
            ('/edit', Edit),
            ('/editConfirm', EditConfirm),
            ('/delete', Delete),
            ('/compare', Compare),
            ('/compareDetails', CompareDetails),
            ('/addReview', AddReview),
            ('/confirmReview', ConfirmReview),
            ],debug=True)
