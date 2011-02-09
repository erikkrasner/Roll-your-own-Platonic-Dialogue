import os
import cgi
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import plato_writer

class MainPage(webapp.RequestHandler):
    def get(self):
        characters = open('datafiles/characters.txt','r').read().split(',')
        template_values = {'characters':characters}
        html = template.render('plato.html', template_values)
        self.response.out.write(html)

application = webapp.WSGIApplication([
        ('/',MainPage)
],debug=True)

def main():
    wsgiref.handlers.CGIHandler().run(application)
