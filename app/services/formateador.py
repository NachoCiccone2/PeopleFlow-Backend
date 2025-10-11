from ..models.empleado_model import Empleado
from bson.objectid import ObjectId
from pymongo.cursor import Cursor

class Formateador:
    @staticmethod
    def empleado_a_diccionario(empleado: Empleado):
        
        empleado_dic = {
            'nombre': empleado.nombre,
            'apellido': empleado.apellido,
            'email': empleado.email,
            'puesto': empleado.puesto,
            'salario': empleado.salario,
            'fecha_ingreso': empleado.fecha_ingreso
        }

        if empleado.id and isinstance(empleado.id, ObjectId):
            empleado_dic['_id'] = empleado.id

        return empleado_dic
    
    @staticmethod
    def empleado_a_JSON(empleado: Empleado):
        empleado_json = Formateador.empleado_a_diccionario(empleado)
        if '_id' in empleado_json:
            empleado_json['id'] = str(empleado_json.pop('_id'))

        return empleado_json
    
    @staticmethod
    def documentoMongo_a_empleado(doc):
        if not doc:
            return None
        
        return Empleado(
            nombre=doc.get('nombre'),
            apellido=doc.get('apellido'),
            email=doc.get('email'),
            puesto=doc.get('puesto'),
            salario=doc.get('salario'),
            fecha_ingreso=doc.get('fecha_ingreso'),
            id=doc.get('_id')
        )
    
    @staticmethod
    def cursor_a_lista(cursor: Cursor):
        lista_empleados = []
        
        for empleado in cursor:
            if '_id' in empleado:
                empleado['id'] = str(empleado.pop('_id'))
            
            lista_empleados.append(empleado)
            
        return lista_empleados