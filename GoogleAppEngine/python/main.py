# -*- coding: utf-8 -*-

from google.appengine.ext import vendor
vendor.add('lib')

import os.path
import webapp2
import jinja2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__), 'templates/')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class HomeView(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())


app = webapp2.WSGIApplication(
    routes=[
        (r'/', HomeView),
    ],
    debug=True
)
