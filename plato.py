import os
import cgi
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import plato_writer

class Dialogue(db.Model):
    id = db.StringProperty()
    characters = db.StringProperty()
    text = db.StringProperty(multiline=True)

class MainPage(webapp.RequestHandler):
    def get(self):
        id = self.request.get('id')
        characters = open('datafiles/characters.txt','r').read().split(',')
        template_values = {'id':id,'characters':characters}
        html = template.render('plato.html', template_values)
        self.response.out.write(html)

class ResultGenerator(webapp.RequestHandler):
    def getID(self):
        return 1
    def post(self):
        id = self.getID()
        self.redirect("/?id=%d" % id)

application = webapp.WSGIApplication([
        ('/',MainPage),
        ('/result',ResultGenerator)
],debug=True)

def main():
    wsgiref.handlers.CGIHandler().run(application)
