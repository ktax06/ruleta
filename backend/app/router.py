from flask import Blueprint, jsonify, current_app, request
from app.DB.sorteos import subir_sorteo, obtener_sorteos
from app.DB.estadisticas import obtener_estadisticas

# Crear un Blueprint para las rutas de init
init_bp = Blueprint('init', __name__)


# Ruta para obtener saludo
@init_bp.route('/', methods=['GET'])
def get_saludo():
    current_app.logger.info("GET request to /")
    data = {
        'message': 'Hola, esta es la API de la aplicación ruleta2.0',
        'status': 'success'
    }
    return jsonify(data), 200   

# ruta para obtener sorteos guardados
@init_bp.route('/obtener/sorteos', methods=['GET'])
def get_sorteos():
    current_app.logger.info("GET request to /obtener/sorteos")
    data = obtener_sorteos()
    if data is None:
        return jsonify({'error': 'No se encontraron sorteos'}), 404
    current_app.logger.info("Sorteos obtenidos correctamente")
    return jsonify(data), 200

# ruta para subir un sorteo
@init_bp.route('/subir/sorteo', methods=['POST'])
def post_sorteos():
    current_app.logger.info("POST request to /subir/sorteo")
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400
    res = subir_sorteo(data)
    if res is None:
        return jsonify({'error': 'Error al subir el sorteo'}), 500
    current_app.logger.info("Sorteo subido correctamente")
    return jsonify({'message': res}), 200

# Ruta para obtener estadísticas
@init_bp.route('/obtener/estadisticas', methods=['GET'])
def get_estadisticas():
    current_app.logger.info("GET request to /obtener/estadisticas")
    data = obtener_estadisticas()
    if data is None:
        return jsonify({'error': 'No se encontraron estadísticas'}), 404
    current_app.logger.info("Estadísticas obtenidas correctamente")
    return jsonify(data), 200
    
    