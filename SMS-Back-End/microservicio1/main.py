# -*- coding: utf-8 -*-
import webapp2

## CLASE QUE PROCESA EL RECURSO /alumnos usando una forma estandar de uso  de parámetros.
class Alumnos(webapp2.RequestHandler):

    def get(self):
        self.response.write("Prueba modulo mobile-frontend")


app = webapp2.WSGIApplication([
    ('/alumnos', Alumnos)
], debug=True)
