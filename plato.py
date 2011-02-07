import cgi
import wsgiref.handlers
from google.appengine.ext import webapp

import markov
import plato_parser

class MainPage(webapp.RequestHandler):
    html = open('plato.html', 'r').read()
    print html
    def get(self):
        self.response.out.write(html)

application = webapp.WSGIApplication([
        ('/',MainPage)
],debug=True)

def main():
    wsgiref.handlers.CGIHandler().run(application)
