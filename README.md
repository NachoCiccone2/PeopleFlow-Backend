# Backend PeopleFlow App
API interna diseñada para centralizar y administrar la información de los empleados de la startup PeopleFlow.

Esta aplicación ayudará al área de Recursos Humanos a prevenir los interminables problemas con la documentación, y les dará las herramientas necesarias para gestionar a los empleados de PeopleFlow de manera sencilla! También permitirá obtener un reporte del promedio de los salarios de manera eficiente.

## 🛠️ Stack Tecnológico
* Backend:
    Python 3.11 (Flask) - Gestiona la lógica de negocio y los endpoints de la API

* Persistencia de datos:
    MongoDB - Base de datos que almacena la información de los empleados.
  
* Contenedores
    Docker & Docker Compose - Orquestación completa del entorno (API + DB).

## 🚀 Instalación y Ejecución

### Opción 1: Ejecución con Docker (Recomendada)

### Requisitos:
Necesitas tener instalado únicamente Docker Desktop (o Docker Engine) en tu sistema operativo.

### Pasos para Ejecutar
1. Clona el Repositorio:

```bash
git clone https://github.com/NachoCiccone2/PeopleFlow-Backend.git
cd PeopleFlow-Backend
```

2. Levantar Contenedores:

Desde la raíz del proyecto (donde están Dockerfile y docker-compose.yml), ejecuta:
```bash
docker-compose up --build
```

_La primera ejecución construirá la imagen de Flask y descargará la imagen de MongoDB, lo cual puede tardar unos minutos._

3. Acceso a la API:

La API estará disponible en la siguiente URL base: `http://localhost:5000`

### Opción 2: Ejecución Nativa (Sin Docker)

### Requisitos: 

Debes tener instalado Python 3.11+ y un servidor MongoDB activo y corriendo en `mongodb://localhost:27017/` .

### Pasos para Ejecutar
1. Clona el Repositorio:

```bash
git clone https://github.com/NachoCiccone2/PeopleFlow-Backend.git
cd PeopleFlow-Backend
```

2. Instalar Dependencias:

```bash
# 1. Crear y activar el entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # macOS/Linux

# 2. Instalar las dependencias de Python
pip install -r requirements.txt
```

3. Configurar Entorno:

Asegúrate de que el archivo .env exista en la raíz con la configuración de tu base de datos local.
```bash
MONGO_URL=mongodb://localhost:27017/
DB_NAME=peopleflow_db
```

Y el archivo .flaskenv:

```bash
FLASK_APP=app/app.py
FLASK_ENV=development
FLASK_RUN_PORT=5000
FLASK_RUN_HOST=0.0.0.0
```

4. Ejecutar la Aplicación:
   
Con el entorno virtual activo, usa el comando de Flask:

```bash
flask run
```

5. Acceso a la API: La API estará disponible en `http://127.0.0.1:5000`.

## 🔍 Endpoints Principales
_Todos los endpoints inician con el prefijo `/empleados` ._

| Recurso       | Método        | URL           | Descripcion   |
| ------------- | ------------- | ------------- | ------------- |
| Crear         | `POST`        | `/empleados`  | Registra un nuevo empleado. Requiere un cuerpo JSON con todos los campos (nombre, apellido, email, puesto, salario, fecha_ingreso). |
| Listar        | `GET`         | `/empleados`  | Obtiene la lista de todos los empleados. Soporta los parámetros de consulta ?puesto=<valor> (filtrado) y ?pagina=<num>&limite=<num> (paginación).  |
| Detalle       | `GET`         | `/empleados/<id>`  | Busca y devuelve la información de un empleado específico por su ID.  |
| Actualizar    | `PUT`         | `/empleados/<id>`  | Actualiza la información de un empleado existente (se pueden enviar campos parciales).  |
| Eliminar      | `DELETE`      | `/empleados/<id>`  | Elimina un empleado del registro.  |
| Reporte       | `GET`         | `/empleados/salarios/promedio`  | Devuelve el promedio de salarios de todos los empleados activos en la base de datos.  |

## ✨ Próximos Pasos 

✅ Uso de Docker para levantar el entorno.

⏳ Documentar la API con Swagger/OpenAPI/Postman.

⏳ Implementar autenticación simple (ej: JWT).

⏳ Incluir tests unitarios (pytest u otro).
