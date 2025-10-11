from ..services.gestor_db_empleados import gestor_db_empleados
from ..services.formateador import Formateador
from ..models.empleado_model import Empleado
from ..exceptions.excepciones import EmpleadoDuplicadoError, EmpleadoNoEncontradoError

class Gestor_Empleados:    
    def __init__(self):
        self.repo = gestor_db_empleados

    def crear(self, empleado: Empleado):
        if self.repo.obtener_por_email(empleado.email):
            raise EmpleadoDuplicadoError(f"El email '{empleado.email}' ya está registrado.")
        
        empleado_dict = Formateador.empleado_a_diccionario(empleado)
        empleado.id = self.repo.crear(empleado_dict)
        return empleado

    def obtener_empleados(self, puesto: str = None, page: int = 1, limit: int = 10):
        filtro_db = {}
        
        if puesto:
            filtro_db['puesto'] = puesto

        empleados_cursor = self.repo.obtener_empleados(filtro=filtro_db, page=page, limit=limit)
        lista_empleados = Formateador.cursor_a_lista(empleados_cursor)

        total_empleados = self.repo.contar_empleados(filtro=filtro_db)
        
        total_paginas = (total_empleados + limit - 1) // limit if total_empleados > 0 and limit > 0 else 0

        return {
            'empleados': lista_empleados,
            'total_registros': total_empleados,
            'pagina_actual': page,
            'limite': limit,
            'total_paginas': total_paginas
        }

    def obtener_por_id(self, empleado_id):
        empleado = self.repo.obtener_por_id(empleado_id)
        if not empleado:
            raise EmpleadoNoEncontradoError("ID invalido o empleado no encontrado.")
        
        if '_id' in empleado:
            empleado['id'] = str(empleado.pop('_id')) 

        return empleado
    
    def actualizar_empleado(self, empleado_id, datos_a_actualizar):
        if("email" in datos_a_actualizar):
            nuevo_email = datos_a_actualizar["email"]
            empleado_con_mismo_email = self.repo.obtener_por_email(nuevo_email)
            if (empleado_con_mismo_email):
                id_encontrado_str = str(empleado_con_mismo_email.get('_id'))
                if id_encontrado_str != empleado_id:
                    raise EmpleadoDuplicadoError(f"El email '{nuevo_email}' ya esta registrado.")
        
        empleado_actualizado = self.repo.actualizar_empleado(empleado_id, datos_a_actualizar)

        if empleado_actualizado is None:
            raise EmpleadoNoEncontradoError("Empleado no encontrado o ID invalido.")
        
        if '_id' in empleado_actualizado:
            empleado_actualizado['id'] = str(empleado_actualizado.pop('_id')) 

        return empleado_actualizado

    def eliminar_empleado(self, empleado_id):
        deleted_count = self.repo.eliminar_empleado(empleado_id)
        if deleted_count == 0:
            raise EmpleadoNoEncontradoError("Empleado no encontrado o ID invalido.")
        return
    
    def obtener_promedio_salarios(self):
        return self.repo.calcular_promedio_salarios()

gestor_empleados = Gestor_Empleados()
