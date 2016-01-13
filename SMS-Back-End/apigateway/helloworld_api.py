# -*- coding: utf-8 -*-
"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""


import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
import os

import jsonpickle


# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID


package = 'Hello'



class MensajeRespuesta(messages.Message):
    message = messages.StringField(1)


class MensajePeticion(messages.Message):
    message = messages.StringField(1)
'''
Como vemos, no aparecen argumentos en el cuerpo de la petición ya que se trata
de una petición de tipo GET.
'''

class Alumno(messages.Message):
    nombre = messages.StringField(1)
    dni = messages.StringField(2)

class ListaAlumnos(messages.Message):
    alumnos = messages.MessageField(Alumno, 1, repeated=True)


class Greeting(messages.Message):
    """Greeting that stores a message."""
    message = messages.StringField(1)

class GreetingCollection(messages.Message):
    """Collection of Greetings."""
    items = messages.MessageField(Greeting, 1, repeated=True)


STORED_GREETINGS = GreetingCollection(items=[
    Greeting(message='hello world!'),
    Greeting(message='goodbye world!'),
])


@endpoints.api(name='helloworld', version='v1')

class HelloWorldApi(remote.Service):
    """Helloworld API v1."""

    MULTIPLY_METHOD_RESOURCE = endpoints.ResourceContainer(
            Greeting,
            times=messages.IntegerField(2, variant=messages.Variant.INT32,
                                        required=True))

    @endpoints.method(MULTIPLY_METHOD_RESOURCE, Greeting,
                      path='hellogreeting/{times}', http_method='POST',
                      name='greetings.multiply')


    def greetings_multiply(self, request):
        return Greeting(message=request.message * request.times)


######################

    '''
    # curl -X GET localhost:8080/_ah/api/helloworld/v1/hellogreeting
    @endpoints.method(message_types.VoidMessage, GreetingCollection,
                      #path=nombre del recurso a llamar
                      path='hellogreeting', http_method='GET',
                      #Puede que sea la forma en la que se llama desde la api:
                      #response = service.greetings().listGreeting().execute()
                      name='greetings.listGreeting')
    def greetings_list(self, unused_request):
        return STORED_GREETINGS
    '''

    @endpoints.method(message_types.VoidMessage, ListaAlumnos,
                      #path=nombre del recurso a llamar
                      path='hellogreeting', http_method='GET',
                      #Puede que sea la forma en la que se llama desde la api:
                      #response = service.greetings().listGreeting().execute()
                      name='greetings.listGreeting')
    def greetings_list(self, unused_request):
        print ("Llamando a una función específica")

        #Conexión a un microservicio específico:

        from google.appengine.api import modules
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        import urllib2
        from google.appengine.api import modules

        #Le decimos al microservicio que queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL sola.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el servicio al que queremos conectarnos.
        url+="alumnos"
        print str(url)
        #result = urllib2.urlopen(url)
        #print result

        #Envío de su resultado

        from google.appengine.api import urlfetch

        #Llamamos al microservicio y recibimos los resultados con URLFetch
        result = urlfetch.fetch(url)

        #Vamos a intentar consumir los datos en JSON y convertirlos a un mensje enviable :)

        print "IMPRESION DE LOS DATOS RECIBIDOS"
        print result.content
        listaAlumnos = jsonpickle.decode(result.content)

        for alumno in listaAlumnos:
            print "nombre: "+str(alumno.get('nombre'))
            print "dni: "+str(alumno.get('dni'))

        '''
        miListaAlumnos=ListaAlumnos()
        miListaAlumnos.alumnos = listaAlumnos
        '''

        alumnosItems= []

        for alumno in listaAlumnos:
            alumnosItems.append(Alumno( nombre=str(alumno.get('nombre')), dni=str(alumno.get('dni'))  ))

        '''
        greetingItems.append(Greeting(message='hello world2'))
        greetingItems.append(Greeting(message='goodbye world2'))
        STORED_GREETINGS2=GreetingCollection(items=greetingItems)
        '''

        #Los adaptamos al tipo de mensaje y enviamos
        #return Greeting(message=str(result.content))
        return ListaAlumnos(alumnos=alumnosItems)


##################




    ID_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            id=messages.IntegerField(1, variant=messages.Variant.INT32))


    @endpoints.method(ID_RESOURCE, Greeting,
                      path='hellogreeting/{id}', http_method='GET',
                      name='greetings.getGreeting')


    def greeting_get(self, request):
        try:
            return STORED_GREETINGS.items[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Greeting %s not found.' %
                                              (request.id,))

    @endpoints.method(message_types.VoidMessage, Greeting,
                      path='hellogreeting/authed', http_method='POST',
                      name='greetings.authed')
    def greeting_authed(self, request):
        current_user = endpoints.get_current_user()
        email = (current_user.email() if current_user is not None
                 else 'Anonymous')
        return Greeting(message='hello %s' % (email,))


APPLICATION = endpoints.api_server([HelloWorldApi])