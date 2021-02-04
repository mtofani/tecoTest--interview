from DBMongo import DBMongo
import datetime
import os
from dotenv import load_dotenv


class Loader(object):

    def __init__(self):

        self.name = "Loader"
        self.URL = os.getenv('URL_DB')
        self.DATABASE = os.getenv('DATABASE')
        self.LOGFILE = os.getenv('LOGFILE')

    def cargarNotasAlumnos(self):
        try:

            print("###PRECARGA NOTAS ALUMNOS####")
            mongo = DBMongo(self.URL, self.DATABASE)
            cursor = mongo.db["notas"]

            post_1 = {
                '_id': 103,
                'date': datetime.datetime(2015, 11, 28),
                'id_alumno': 1,
                'nota': 6,
                'id_materia': 1,
                'nombreMateria': "IT"
            }

            post_2 = {
                '_id': 102,
                'id_alumno': 2,
                'date': datetime.datetime(2015, 11, 28),
                'nota': 6,
                'id_materia': 1,
                'nombreMateria': "IT"

            }
            post_3 = {
                '_id': 100,
                'date': datetime.datetime(2018, 11, 28),
                'id_alumno': 2,
                'nota': 4,
                'id_materia': 2,
                'nombreMateria': "Estadistica"
            }

            post_4 = {
                '_id': 104,
                'date': datetime.datetime(2020, 11, 28),
                'id_alumno': 2,
                'nota': 8,
                'id_materia': 2,
                'nombreMateria': "Estadistica"
            }

            post_5 = {
                '_id': 105,
                'date': datetime.datetime(2019, 11, 28),
                'id_alumno': 2,
                'nota': 9,
                'id_materia': 2,
                'nombreMateria': "Estadistica"
            }
            post_6 = {
                '_id': 107,
                'date': datetime.datetime(2019, 11, 28),
                'id_alumno': 2,
                'nota': 11,
                'id_materia': 2,
                'nombreMateria': "Estadistica"
            }

            post_7 = {
                '_id': 108,
                'date': datetime.datetime(2021, 11, 28),
                'id_alumno': 1,
                'nota': 10,
                'id_materia': 1,
                'nombreMateria': "IT"
            }

            post_7 = {
                '_id': 109,
                'date': datetime.datetime(2022, 11, 2),
                'id_alumno': 1,
                'nota': 6,
                'id_materia': 1,
                'nombreMateria': "IT"
            }

            post_8 = {
                '_id': 110,
                'date': datetime.datetime(2022, 11, 2),
                'id_alumno': 1,
                'nota': 7,
                'id_materia': 2,
                'nombreMateria': "Estadistica"
            }

            post_9 = {
                '_id': 111,
                'date': datetime.datetime(2022, 11, 2),
                'id_alumno': 1,
                'nota': 7,
                'id_materia': 2,
                'nombreMateria': "Estadistica"
            }

            post_10 = {
                '_id': 112,
                'date': datetime.datetime(2022, 11, 2),
                'id_alumno': 1,
                'nota': 7,
                'id_materia': 2,
                'nombreMateria': "Estadistica"
            }

            post_11 = {
                '_id': 113,
                'date': datetime.datetime(2022, 11, 2),
                'id_alumno': 1,
                'nota': 7,
                'id_materia': 3,
                'nombreMateria': "REDES"
            }

            post_12 = {
                '_id': 114,
                'date': datetime.datetime(2022, 11, 2),
                'id_alumno': 2,
                'nota': 7,
                'id_materia': 3,
                'nombreMateria': "REDES"
            }

            post_13 = {
                '_id': 115,
                'date': datetime.datetime(2019, 11, 2),
                'id_alumno': 2,
                'nota': 8,
                'id_materia': 3,
                'nombreMateria': "REDES"
            }

            new_result = cursor.insert_many(
                [post_1, post_2, post_3, post_4, post_5, post_6, post_7, post_8, post_9, post_10, post_11, post_12, post_13])
            # b = cursor.delete_many({})

            return print('Multiple posts: {0}'.format(new_result.inserted_ids))

        except Exception as e:
            print("OCURRIO ERROR EN CARGA DE NOTAS")

        finally:
            mongo.cerrarMongo()

    def cargarAlumnos(self):

        try:
            print("###PRECARGA  ALUMNOS####")
            mongo = DBMongo(self.URL, self.DATABASE)
            cursor = mongo.db["alumnos"]

            post_1 = {
                '_id': 1,
                'nombre': 'Maxi',
                'apellido': 1,
                'dni': 1,
                'sexo': "Masc",
                'materias': [1, 2, 3]
            }

            post_2 = {
                '_id': 2,
                'nombre': 'Carlos',
                'apellido': 1,
                'dni': 1,
                'sexo': "Masc",
                'materias': [1, 2, 3]

            }

            new_result = cursor.insert_many([post_1, post_2, ])
            mongo.cerrarMongo()
            return print('Multiple posts: {0}'.format(new_result.inserted_ids))

        except Exception as e:
            print("OCURRIO ERROR EN CARGA DE NOTAS")

        finally:
            mongo.cerrarMongo()

    def purgarDatos(self):

        try:
            print("###BORRANDO ALUMNOS####")

            mongo = DBMongo(self.URL, self.DATABASE)
            cursor = mongo.db["alumnos"]
            b = cursor.delete_many({})
            print("###BORRANDO NOTAS ####")
            mongo = DBMongo(self.URL, self.DATABASE)
            cursor = mongo.db.notas
            b = cursor.delete_many({})
            self.cargarAlumnos()
            self.cargarNotasAlumnos()

        except Exception as e:
            print("OCURRIO ERROR EN PURGADO DE DATOS"+str(e))

        finally:
            mongo.cerrarMongo()
