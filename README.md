
# TestTeco
Challenge 
## Instalación


```bash
Una vez obtenido el proyecto, 
pip install -r requirements.txt
```


## Documentacion
 [SwaggerDOC](http://127.0.0.1:5000/) - Puerto 5000 localhost, esta toda la documentacion de como utilizar la API de la APP.

## Arquitectura - Diseño

Si bien estoy en proceso a de moverme finalmente a JavaScript para este caso opté  por las siguientes tecnologias : 
**Framework**: Flask RESTx - API  [RESTX](https://flask-restx.readthedocs.io/en/latest/)

**DB**: Con el fin de explorar un poco mas, elegí MongoDB ya que solo habia hechos algunas pruebas, me parecia divertido para sumarme al desafio, de haber trabajado siempre con SQL y afines.

Se tienen dos colecciones de datos en la base "secundaria" ( alumnos y notas). Dentro de alumno hay un arreglo de materias.

## Alcance
1) Esta fuera de alcance en esta prueba, la confiabilizacion de los datos. Se asume que hay integridad de ID's entre las Entidades. (_Alumno-Materias/Notas_). 

2) Fuera de alcance el frontEnd del Portal. En su "lugar" utilicé el framework Restx (simplificando varias cosas) que agiliza la documentacion con algunos en algunos tags, dando la posilidad de presentarle la info sea en un sitio web o mismo con el file .swagger.json a un equipo /o dev dedicado al front con modelos, utilizacion de la API parametros etc.

**Si tuviera que armarlo hoy ...  lo haría en React. y usaría solo el back Rest de Python si es necesario. 
 ya que da  mucha mas agilidad para desarrollar con componentes vs el/los motores de template usa Flask.*
 
## Utilización 
Se debe ejecutar el app.py, y probar desde [API](http://127.0.0.1:5000/).
Los datos ya estan cargados, por medio de la clase Loader.

Si quieren emular la carga desde 0, se puede llamar al metodo purgarDatos() del main.

Los EP que resuelven los puntos son: 

/api/v1/getResumenAlumno/{id}


​/api​/v1​/modificarDatosAlumno​/

## Ejemplo - Casos Test

#### http://127.0.0.1:5000/api/v1/getResumenAlumno/1

```json
{
  "Alumno": {
    "_id": 1,
    "apellido": 1,
    "dni": 1,
    "nombre": "Maxi",
    "sexo": "Masc"
  },
  "message": {
    "materia1 ": [
      6,
      6
    ],
    "materia2 ": [
      7,
      7,
      7
    ],
    "materia3 ": [
      7
    ]
  }
}
```
#### /api/v1/modificarDatosAlumno/
```json

  "id": 1,
  "nombre": "Nuevo nombre",
  "apellido": "Apellido!",
  "sexo": "Masc",
  "estadoCivil": "Solt",
  "dni": "36999123"
}
```     
Response OK: 
```json
{
  "message": "Datos modificados OK registro:  ID: 1"
}
```

Response FAIL: 
```json
{
  "message": "Error al modificar registro con id: 1"
}
```

### Para las pruebas ya estan creados dos alumnos de ID, 1 y 2 ###

## Mejoras
1) El proyecto se debería  estructurar y subdividir mas folders, en rutas, controllers, view (si corresponde PY)  , db,  namespaces etc.. Por los tiempos, claramente fui por lo mas resumido posible.
2) Manejar mas validaciones de error en los EP y entradas, autenticacion mediante token o al menos un basic-auth. 

3) Realizar Test cruzado/Revisiones mas alla del unit.
4) El el modelo de datos no incluí la coleccion "Materias"  en si, porque no hizo falta para resolver la problematica de test. Claramente en un entorno real, hubiese participado en algunas operaciones y lo reemplace por un Array en la coleccion de alumnos.
5) Guardar los request en una DB en vez del log de la app. Para saber quien me consume y que servicios.
6) Un importer masivo, desde archivos.
entre otras..

## Conclusión
Mas alla de la propuesta en si, cuenten conmigo para cualquier tema de nuevas tecnologías. Ya que es interesante estar en contacto con colegas de las telco e intercambiar experiencias e info.

Gracias!
