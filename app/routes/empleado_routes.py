from flask import Blueprint, request, jsonify

from ..services.gestor_empleados import gestor_empleados
from ..services.formateador import Formateador
from ..services.validador import Validador
from ..exceptions.excepciones import EmpleadoDuplicadoError, EmpleadoNoEncontradoError

empleado_bp = Blueprint('empleados', __name__, url_prefix='/empleados')

@empleado_bp.route('/', methods=['POST'])
def crear_empleado():
    try:
        data = request.json
        nuevo_empleado = Validador.validar_nuevo_empleado(data)
        empleado_creado = gestor_empleados.crear(nuevo_empleado)
        return jsonify(Formateador.empleado_a_JSON(empleado_creado)), 201

    except EmpleadoDuplicadoError as e:
        return jsonify({'error': str(e)}), 409
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error al crear empleado: {str(e)}'}), 500

@empleado_bp.route('/', methods=['GET'])
def listar_empleados():
    try:
        puesto = request.args.get('puesto')
        page_str = request.args.get('page', '1')
        limit_str = request.args.get('limit', '10')

        page,limit = Validador.validar_paginacion(page_str,limit_str)        

        resultado_paginado = gestor_empleados.obtener_empleados(
            puesto=puesto, 
            page=page, 
            limit=limit
        )
        
        return jsonify(resultado_paginado), 200
    except ValueError as e:
            return jsonify({'error': f'Parámetros de paginación inválidos: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error al obtener empleados: {str(e)}'}), 500
    
@empleado_bp.route('/<string:empleado_id>', methods=['GET'])
def obtener_empleado_por_id(empleado_id):
    try:
        empleado = gestor_empleados.obtener_por_id(empleado_id)
        return jsonify(empleado), 200
    except EmpleadoNoEncontradoError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Error al obtener empleado: {str(e)}'}), 500
    
@empleado_bp.route('/<string:empleado_id>', methods=['DELETE'])
def eliminar_empleado(empleado_id):
    try:
        gestor_empleados.eliminar_empleado(empleado_id)
        
        return jsonify({'message': f'Empleado con ID {empleado_id} eliminado con exito.'}), 200
    
    except EmpleadoNoEncontradoError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Error al eliminar empleado: {str(e)}'}), 500
    
@empleado_bp.route('/<string:empleado_id>', methods=['PUT'])
def actualizar_empleado(empleado_id):
    try:
        data = request.json
        
        datos_a_actualizar, error_validacion = Validador.validar_datos_actualizacion(data)

        if error_validacion:
            return jsonify({'error': error_validacion}), 400

        empleado_actualizado = gestor_empleados.actualizar_empleado(empleado_id, datos_a_actualizar)

        return jsonify(empleado_actualizado), 200
    
    except EmpleadoDuplicadoError as e:
        return jsonify({'error': str(e)}), 409
    except EmpleadoNoEncontradoError as e:
        return jsonify({'error': str(e)}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 400 
    except Exception as e:
        return jsonify({'error': f'Error interno al actualizar empleado: {str(e)}'}), 500
    
@empleado_bp.route('/salarios/promedio', methods=['GET'])
def obtener_promedio_salarios():
    try:
        promedio = gestor_empleados.obtener_promedio_salarios()
        
        return jsonify({ 'promedio_salarios': round(promedio, 2)}), 200

    except Exception as e:
        return jsonify({'error': f'Error al calcular promedio: {str(e)}'}), 500