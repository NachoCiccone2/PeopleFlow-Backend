from ..db.db import db
from bson.objectid import ObjectId
from pymongo import ReturnDocument

class Gestor_DB_Empleados:
    def __init__(self):
        self.collection = None

    def inicializar_coleccion (self):
        if db.db is None:
            raise ConnectionError("La conexión a la base de datos no está establecida.")
        self.collection = db.db['empleados']

    def crear(self, empleado: dict):
        result = self.collection.insert_one(empleado)
        empleado_id = result.inserted_id
        return empleado_id
    
    def obtener_empleados(self, filtro: dict = None, page: int = 1, limit: int = 10):
        if filtro is None:
            filtro = {}

        skip = (page - 1) * limit
        cursor = self.collection.find(filtro)
        cursor = cursor.skip(skip).limit(limit)

        return cursor
    
    def contar_empleados(self, filtro: dict = None):
        if filtro is None:
            filtro = {}
        return self.collection.count_documents(filtro)

    def obtener_por_id(self, empleado_id: str):            
        try:
            oid = ObjectId(empleado_id)
        except Exception:
            return None 
        
        return self.collection.find_one({'_id': oid})
    
    def obtener_por_email(self, email: str):            
        return self.collection.find_one({'email': email})

    def eliminar_empleado(self, empleado_id: str):            
        try:
            oid = ObjectId(empleado_id)
        except Exception:
            return 0

        resultado = self.collection.delete_one({'_id': oid})

        return resultado.deleted_count 

    def actualizar_empleado(self, empleado_id: str, datos_a_actualizar: dict):        
        try:
            oid = ObjectId(empleado_id)
        except Exception:
            return 0

        resultado = self.collection.find_one_and_update(
            {'_id': oid},
            {'$set': datos_a_actualizar},
            return_document=ReturnDocument.AFTER
        )

        return resultado
    
    def calcular_promedio_salarios(self):
        pipeline = [
            { '$group': { '_id': None, 'promedio': {'$avg': '$salario'} } },
            { '$project': { '_id': 0, 'promedio': 1 } }
        ]

        cursor_resultado = self.collection.aggregate(pipeline)

        resultado = list(cursor_resultado)

        if not resultado:
            return 0.0

        return resultado[0]['promedio']
    
gestor_db_empleados = Gestor_DB_Empleados()