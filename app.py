from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_restx import Resource, Api, Namespace,  fields, reqparse
from DBMongo import DBMongo
import datetime
from bson.objectid import ObjectId
import bson.json_util
from bson.json_util import dumps, loads
import json
import os
import logging
from Loader import *


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
api = Api(app)
ns1 = api.namespace('api/v1', description='API SECUNDARIA')

# una vez cargados los valores, podemos usarlos

alumnoModel = api.model('Alumno', {
    'id': fields.Integer(required=True),
    'nombre': fields.String(required=True),
    'apellido': fields.String(required=True),
    'sexo': fields.String(required=True),
    'estadoCivil': fields.String(required=True),
    'dni': fields.String(required=True)

})


def logear(log, msg):

    log(str(datetime.datetime.now())+" "+msg+"  from: "+str(request.remote_addr))


class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


## RUTAS - CONTROLLERS ##

@ ns1.route('/getdatosAlumnos/<int:id>', endpoint='datosAlumnos')
@ ns1.doc(params={'id': ' ID del alumno'})
class datosAlumno(Resource):
    def get(self, id):

        try:

            logear(app_log, "CONSULTA => "+str(request.url))
            mongo = DBMongo(URL, DATABASE)
            cursor = mongo.db.alumnos

            # No muestro el array de materias
            record = cursor.find_one({'_id': id}, {"materias": 0})
            if record:
                return jsonify(record)

            else:
                return {'message': "Sin datos para esa consulta"}

        except Exception as e:
            logear(app_log, "ERROR al obtener informacion")
            return {'message': "Error al consultar informacion alumnos"}

        finally:
            mongo.cerrarMongo()


@ ns1.route('/getallAlumnos')
class getallAlumnos(Resource):
    def get(self):

        try:

            logear(app_log, "CONSULTA => "+str(request.url))

            mongo = DBMongo(URL, DATABASE)
            cursor = mongo.db.alumnos
            records = cursor.find({})
            list_cur = list(records)

            if(list_cur):
                return jsonify(list_cur)

            else:
                return {'message': "Sin datos para esa consulta"}

        except Exception as e:
            logear(app_log, "ERROR al obtener informacion")
            return {'message': "Error al consultar informacion alumnos"}

        finally:
            mongo.cerrarMongo()


@ns1.route('/getNotasAlumno/<int:id>')
class Examenes(Resource):
    def get(self, id):
        try:
            logear(app_log, "CONSULTA => "+str(request.url))
            mongo = DBMongo(URL, DATABASE)
            cursor = mongo.db.notas
            records = cursor.find({'id_alumno': id}).sort(
                [("id_materia", 1), ("date", -1)])

            list_cur = list(records)

            if (list_cur):
                return jsonify(list_cur)

            else:
                return {'message': "Sin datos para esa consulta"}

        except Exception as e:
            logear(app_log, "ERROR al obtener informacion alumno: "+str(e))
            return {'message': "Error al consultar informacion"}

        finally:
            mongo.cerrarMongo()


@ns1.route('/getResumenAlumno/<int:id>')
class Resumen(Resource):
    def get(self, id):

        try:
            logear(app_log, "CONSULTA => "+str(request.url))
            mongo = DBMongo(URL, DATABASE)
            # TRAIGO INFO DE ESE ALUMNO
            cursor = mongo.db["alumnos"]
            record = cursor.find_one({'_id': id})

            # TRAIGO NOTAS
            cursor = mongo.db["notas"]
            records = cursor.find({'id_alumno': id}).sort(
                [("id_materia", 1), ("date", -1)])
            list_cur = list(records)

            # POSTPROCESO DE ULTIMAS NOTAS DE CADA MATERIA
            results = []
            umbralNotas = 4
            data = {}

            # dejo esto Para probar un !NOT
            if (record['materias']):
                materias = record['materias']
            else:
                materias = [1, 2, 3]

            logear(app_log, "Procesando datos del alumno: "+str(id))
            for m in materias:

                logear(app_log, "INICIO MATERIA:"+str(m))
                cantNotas = 0

                for row in list_cur:

                    if row['id_materia'] == m and cantNotas < umbralNotas:
                        results.append(row['nota'])
                        print(row['nota'])
                        cantNotas += 1
                logear(app_log, "FIN MATERIA:"+str(m))
                logear(app_log, "NOTAS :"+str(results))
                salida = " 'materia'"+str(m)+": "+str(results)

                # Si Tengo datos en esa materia, genero el array de notas
                if results:
                    data['materia'+str(m)+" "] = results

                results = []

            # Armo el JSON de salida

            json_data = json.dumps(data)
            print(json_data)

            json_salida = {
                'Alumno': record,
                'message': data

            }

            if (record):
                return jsonify(json_salida)
            else:
                return {'message': "Sin datos del alumno"}

        except Exception as e:
            logear(app_log, "Error al obtener informacion alumno"+str(e))
            return {'message': "Error al consultar informacion"}

        finally:
            mongo.cerrarMongo()

        # return jsonify(record, data)


@ ns1.route('/getAllNotas')
class AllExamenes(Resource):

    def get(self):

        try:
            logear(app_log, "CONSULTA => "+str(request.url))
            mongo = DBMongo(URL, DATABASE)
            cursor = mongo.db["notas"]
            records = cursor.find({}).sort(
                [("id_materia", 1), ("date", -1)])
            list_cur = list(records)

            if (list_cur):
                return jsonify(list_cur)
            else:

                return {'message': "Sin datos para esa consulta"}

        except Exception as e:
            logear(app_log, "Error al obtener informacion alumno"+str(e))
            return {'message': "Error al consultar informacion"}

        finally:
            mongo.cerrarMongo()

# MODIFICAR ALUMNO


@ ns1.route('/modificarDatosAlumno/')
class ModificarDatosAlumno(Resource):
    @ ns1.doc(body=alumnoModel)
    def post(self):
        try:

            logear(app_log, "MODIFICACION => "+str(request.url))
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=int, location='json')
            parser.add_argument('nombre', type=str, location='json')
            parser.add_argument('apellido', type=str, location='json')
            parser.add_argument('sexo', type=str, location='json')
            parser.add_argument('estadoCivil', type=str, location='json')
            parser.add_argument('dni', type=str, location='json')
            args = parser.parse_args()

            # MAPEO ? VALID
            nombre = args['nombre']
            id = int(args['id'])
            ap = args['apellido']
            sexo = args['sexo']
            ec = args['estadoCivil']
            dni = args['dni']

            mongo = DBMongo(URL, DATABASE)
            cursor = mongo.db["alumnos"]
            myquery = {"_id": id}
            newvalues = {"$set": {"nombre": nombre, "apellido": ap,
                                  "sexo": sexo, "estadoCivil": ec, "dni": dni}}
            result = cursor.update_one(myquery, newvalues)
            if (result.modified_count == 1):
                logear(app_log, "SE MODIFICO REGISTRO ALUMNO , ID:" +
                       str(id)+str(request.url))
                return {'message': "Datos modificados OK registro:  ID: "+str(id)}
            else:
                logear(app_log, "ERROR AL MODIFICAR REGISTRO, VERIFICAR DATOS EN CARGA, ID :" +
                       str(id)+str(request.url))
                return {'message': "Error al modificar registro con id: "+str(id)}

        except Exception as e:
            print("ACA")
            logear(app_log, "ERROR EN MODIFICACION DE DATOS ALUMNO. "+str(e))
            return {'message': "ERROR en modificacion "}

        finally:
            mongo.cerrarMongo()

    # MAIN


# Loader carga los datos de prueba.
# TPurgar BORRA y carga los datos para el test
if __name__ == '__main__':

    load_dotenv()
    app.json_encoder = JSONEncoder
    URL = os.getenv('URL_DB')
    DATABASE = os.getenv('DATABASE')
    LOGFILE = os.getenv('LOGFILE')
    fh = logging.FileHandler(LOGFILE)
    ns1.logger.addHandler(fh)
    app_log = ns1.logger.info

    l = Loader()
    l.purgarDatos()

    app.run(debug=True, use_reloader=True)
