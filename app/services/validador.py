import re
from ..models.empleado_model import Empleado

class Validador:
    @staticmethod
    def validar_nuevo_empleado(data):
        campos_obligatorios = ['nombre', 'apellido', 'email', 'puesto', 'salario', 'fecha_ingreso']
        for campo in campos_obligatorios:
            if (campo not in data) or (data[campo] is None):
                raise ValueError(f"El campo '{campo}' es obligatorio.")
            
        if( not Validador.validar_email(data['email']) ):
            raise ValueError("Email con formato invalido.")

        if( not Validador.validar_fecha(data['fecha_ingreso']) ):
            raise ValueError("Fecha con formato invalido.")
        
        nuevo_empleado = Empleado(
            nombre=data['nombre'],
            apellido=data['apellido'],
            email=data['email'],
            puesto=data['puesto'],
            salario=float(data['salario']),
            fecha_ingreso=data['fecha_ingreso']
        )

        return nuevo_empleado
    
    @staticmethod
    def validar_datos_actualizacion(data):
        campos_permitidos = ['nombre', 'apellido', 'email', 'puesto', 'salario', 'fecha_ingreso']
        datos_a_actualizar = {}

        for key, value in data.items():
            if (key in campos_permitidos) and (value is not None):
                if key == 'email':
                    if not Validador.validar_email(value):
                        return {}, f"Email '{value}' con formato inválido."
                    datos_a_actualizar[key] = value
                
                elif key == 'fecha_ingreso':
                    if not Validador.validar_fecha(value):
                        return {}, f"Fecha '{value}' con formato inválido."
                    datos_a_actualizar[key] = value

                elif key == 'salario':
                    datos_a_actualizar[key] = float(value)
                else:
                    datos_a_actualizar[key] = value

        if not datos_a_actualizar:
            return {}, "No se proporcionaron datos validos para actualizar."
        
        return datos_a_actualizar, None
    
    @staticmethod
    def validar_paginacion(page_str,limit_str):
        page = int(page_str)
        limit = int(limit_str)
        if page < 1 or limit < 1:
            raise ValueError("page y limit deben ser numeros positivos.")
        
        return page,limit

    @staticmethod
    def validar_email(email: str) -> bool:
        patron_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(patron_email, email) is not None
    