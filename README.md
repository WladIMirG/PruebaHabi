***GENERALIDADES***

-	Acomodaremos el espacio de trabajo:

        pip install --upgrade pip

- Considere la creacion de un entorno virtual.

- Instale dependencias:

Ubícate con la terminal en le directorio y ejecuta el siguiente comando:

        pip install -r requirements.txt

Se instalarán todos los requerimientos necesarios para este proyecto.



**Ejecucion de la API**

- Importe la base de datos (Recomiendo HeidiSQL) y lancela.

- En la funcion "application" en el "App.py" modifique las credenciales de conexion a la base de datos en "db.run_con()" linea 61.

- La Api se ejecuta por terminal, hubicandose en la carpeta contenedora y con el siguiente comando:

                python App.py

- O ejecute App.py en la interfaz de su editor.

***PROBLEMA 1***

**Análisis**

- No pude revisar la base de datos, sin embargo, imagino que será algo como con una entidad llamada "INMUEBLE" con, por lo menos, los campos de consulta: Ciudad, año, estado.

- Voy a diseñar esta etapa de consulta de la siguiente forma:
1. Un objeto que extraiga la información de la base de datos.
2. Un microservicio que, mediante una petición GET, se le ingresen los datos de Consulta.


**DESARROLLO**

Para abordar el desarrollo de la API dividí el problema de la siguiente manera:

-	Desarrollo de la base de datos.
-	Desarrollar el Web service.
        - Servidor.
        - Api.
-	Gestor de Query’s a la base de datos.



**Base de datos**

Diseñe la base de datos de forma sencilla en un proyecto llamado “db_habi.sql” el cual contiene las bases de datos para departamentos, municipios, estados e inmuebles. Como lo muestra la parte verde del "DiagramaEntidad-Relacion.png" de la carpeta "imag".

Por favor lanzar la base de datos.


**Peticiones a la base de datos**
	
La petición la manejare por medio del módulo de Python “mysql-connector-python==8.0.26” el cual provee gestión para la base de datos. A partir de este módulo se crea una clase “DB_query” el cual se conectará a la base de datos, recibe variable del tipo “Query” que contiene un diccionario con los datos de la petición proveniente del cliente, descompone la petición y crea mediante lenguaje SQL una petición que será pasada a la base de datos. Se podía usar un ORM, sin embargo, se desistió de esta alternativa por las condiciones del ejerció.

**Servidor**

Para recibir las peticiones del cliente se usa el estándar WSGI de Python a través del módulo “wsgiref”, con el cual se construye un servidor confiable.

**API**

Se crea la aplicación que recibe un diccionario “environ” y la función “start_response”, la última recibirá los headers y los estados HTTP para la respuesta. Desde la API se descompone el argumento de la URL y se descompone en un diccionario de tipo “dt.Query” que contiene los parámetros de la petición. También desde esta Aplicación se llamará a la clase “DB_query”, la que se encargará de construir, mediante lenguaje SQL, la petición, a partir de los parámetros de la solicitud. Una vez recibida la respuesta se organizan los datos en un diccionario del tipo “TypedDict”, para que sea más fácil su serialización, se ajusta el filtrado y esta clase devolverá una lista llena de diccionarios, cada uno equivalente a los datos de un inmueble en específico.

**URL raiz**

Para la url no se ve necesario que se construya un path para el ejercicio en concreto. Su raíz estará compusta de la siguiente forma:

http://127.0.0.1:8000/

**Peticiones desde el front**

El Front podrá hacer una peticion de la siguiente forma:

“http://localhost:8000/?city=Amaga&status=En_venta&year=2000&year=2003”

Donde:

**&city=NombreCiudad**: Contendra la peticion de la ciudad, se espera que sea una sola ciudad por peticion, en el caso de que sean mas la aplicación tomara como prioridad la primera.

**&status=estadoRequerido**: El estado requerido puede tomar varias variables y se podra escribir asi: &status=estado1&status=estado2

**&year=año1&year=año2**: De igual forma que la consulta anterior se pueden incorporar múltiples consultas en esta variable.

Nota 1: No se tiene en cuenta el orden con el que se establezcan las variables en la petición.

Con esta petición se genera un archivo con la siguiente estructura:

Query   = 	{“city”: [NombreCiudad],
“estatus”: [estado1, estado2],
“year”:[año1, año2]}

**Response**

La respuesta no es más que un archivo JSON que se le suministrara al cliente y que contiene la información de cada inmueble encontrado, así:

Response = {
0 : {
    "adress": "Cll 1 # 1",
    "city_name": "ABEJORRAL",
    "city_code": 2,
    "status": "En_venta",
    "price": 90000000,
    "descrip": "Casa con 2 habitaciones, 1 ba\u00f1o, sala, comedor y cocina"
   },
1 : {
    "adress": "Cll 1 # 11",
    "city_name": "ABEJORRAL",
    "city_code": 2,
    "status": "En_venta",
    "price": 1000000,
    "descrip": "Casa11"
   },
2 : {
    "adress": "Cll 1 # 13",
    "city_name": "ABEJORRAL",
    "city_code": 2,
    "status": "En_venta",
    "price": 3000000,
    "descrip": "Casa 13"
   }
}

***PROBLEMA 2***

La solución se base en extender la base de datos, creando una nueva tabla que es la que contendrá los “me gusta” que genere cada usuario y a que inmueble se los genera, por lo cual se propone la parte azul del diagrama "DiagramaEntidad-Relacion.png" en la carpeta "imag".

Para hacer la extensión es necesario que se tenga en cuenta las relaciones para la nueva tabla. El código se encuentra en el archivo “me_gusta.sql”