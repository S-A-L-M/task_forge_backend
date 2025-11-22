from flask import Blueprint, request, jsonify
from models.node import Node

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search():
    """Buscar tareas y proyectos"""
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({'error': 'Parámetro de búsqueda requerido'}), 400
        
        results = Node.search(query)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500