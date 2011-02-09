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

class ID(db.Model):
    value = db.StringProperty()

class MainPage(webapp.RequestHandler):
    def get(self):
        id = self.request.get('id')
        characters = open('datafiles/characters.txt','r').read().split(',')
        template_values = {'id':id,'characters':characters}
        html = template.render('plato.html', template_values)
        self.response.out.write(html)

class ResultGenerator(webapp.RequestHandler):
    def getID(self):
        id = db.GqlQuery("SELECT * FROM ID")
        id =id.get()
        if id:
            value = int(id.value)
        else:
            id = ID()
            value = 0
        id.value = str(value + 1)
        db.put(id)
        return value
    def post(self):
        new_dialogue = Dialogue()
        id = self.getID()
        characters = self.request.get_all("character")
        order = self.request.get("order")
        text= PlatoWriter(characters).write(order)
        new_dialogue.id = str(id)
        new_dialogue.characters = reduce(lambda a,b: a+" "+b, characters)
        new_dialogue.order = order
        new_dialogue.text = text
        new_dialogue.put()
        self.redirect("/?id=%d" % id)

application = webapp.WSGIApplication([
        ('/',MainPage),
        ('/result',ResultGenerator)
],debug=True)

def main():
    wsgiref.handlers.CGIHandler().run(application)
