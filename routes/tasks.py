from flask import Blueprint, request, jsonify
from models.node import Node

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Obtener todas las tareas y proyectos"""
    try:
        tasks = Node.get_all()
        return jsonify(tasks), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """Obtener una tarea específica"""
    try:
        node = Node.get_by_id(task_id)
        if node:
            return jsonify(node.to_dict()), 200
        return jsonify({'error': 'Tarea no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """Crear una nueva tarea o proyecto"""
    try:
        data = request.get_json()
        
        # Validación básica
        if not data.get('title'):
            return jsonify({'error': 'El título es requerido'}), 400
        
        node = Node.create(data)
        return jsonify(node.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    """Actualizar una tarea o proyecto"""
    try:
        data = request.get_json()
        node = Node.update(task_id, data)
        
        if node:
            return jsonify(node.to_dict()), 200
        return jsonify({'error': 'Tarea no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Eliminar una tarea o proyecto"""
    try:
        node = Node.get_by_id(task_id)
        if not node:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        
        Node.delete(task_id)
        return jsonify({'message': 'Tarea eliminada correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500