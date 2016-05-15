# -*- coding: utf-8 -*-
from google.appengine.ext import ndb

class Prueba(ndb.Model):
    texto=ndb.StringProperty()

class ControlAsistencia(ndb.Model):

    '''
    Contro de asistencia de un alumno concreto en una clase y asignatura con profesor concretos.
    '''

    # id_ca = ndb.IntegerProperty() --< NO NECESARIO: id_key autoimplementado en ndb
    #Fecha y hora a la que se ha realizado el control de asistencia.
    fecha_hora = ndb.DateTimeProperty()
    #Si el alumno ha asistido a clase
    asistencia = ndb.BooleanProperty()
    #Si ha traido o no el uniforme.
    uniforme = ndb.BooleanProperty()
    #Si el alumno no ha llegado con retraso será un 0, pero puede ser un retraso de 10 min o de 20 min o mas en cuyo caso será 10 o 20 el valor
    retraso = ndb.IntegerProperty()
    #En caso de llegar con retraso de cuanto se ha tratado. 10 o 20 o + minutos
    #retraso_tiempo= ndb.IntegerProperty()
    #En caso de llegar con retraso si este ha sido justificado o no
    retraso_justificado = ndb.BooleanProperty()

    #Datos de los implicados
    id_alumno = ndb.IntegerProperty()
    id_profesor = ndb.IntegerProperty()
    id_clase = ndb.IntegerProperty()
    id_asignatura = ndb.IntegerProperty()

    #Método que devuelve todo lo guardado. En la práctica no se usará

    @classmethod
    def devolver_todo(cls):
        return cls.query().order(-cls.fecha_hora)

#Crear clase NO NDB en un fichero pytthon que sea CA simple y CA complejo. El CA simple tiene estos datos,
#CA complejo tiene estos datos mas lo s nombres de cada uno.
#Se utilizará para devolver los objetos en las funciones

class ResumenControlAsistencia(ndb.Model):

    lista_idCA = ndb.KeyProperty(repeated=True) # La propiedad repeated hace que el campo sea una lista y pueda tomar varios valores, en lugar de solo unof
    fecha_hora = ndb.DateTimeProperty()
    id_profesor = ndb.IntegerProperty()
    id_clase = ndb.IntegerProperty()
    id_asignatura = ndb.IntegerProperty()

class AlumnosNombreID(ndb.Model):
    id_alumno = ndb.IntegerProperty(required=True)
    nombre_alumno = ndb.StringProperty(required=True)

class ProfesoresNombreID(ndb.Model):
    id_profesor = ndb.IntegerProperty(required=True)
    nombre_profesor = ndb.StringProperty(required=True)

class ClasesNombreID(ndb.Model):
    id_clase = ndb.IntegerProperty(required=True)
    nombre_clase = ndb.StringProperty(required=True)

class AsignaturasNombreID(ndb.Model):
    id_asignatura = ndb.IntegerProperty(required=True)
    nombre_asignatura = ndb.StringProperty(required=True)