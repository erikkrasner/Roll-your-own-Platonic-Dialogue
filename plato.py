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
        dialogue = db.GqlQuery("SELECT * FROM Dialogue WHERE id=:1", id)
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
        def structure_dialogue(speech_pair):
            speaker, speech = speech_pair
            return "<p><b>{0}:</b>{1}</p>".format(speaker,speech)
        new_dialogue = Dialogue()
        id = self.getID()
        title = self.request.get("title")
        characters = self.request.get_all("character")
        order = self.request.get("order")
        text_list= PlatoWriter(characters).write(int(order))
        text = "<h2>%s</h2><br>By Plato, trans. Benjamin Jowett with help from Mark V Shaney<br><br>" % title.title()
        text += "Persons of the Dialogue<br>"
        text += reduce(lambda a,b: a + "<br>" + b, map(lambda x: x.upper(),characters))
        text += "<br>-------------<br>"
        text += map(structure_dialogue,text_list)
        text += "<br>THE END"
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
