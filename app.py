from flask import Flask
from flask_cors import CORS
from routes.tasks import tasks_bp
from routes.search import search_bp

app = Flask(__name__)
CORS(app)  

app.register_blueprint(tasks_bp, url_prefix='/api')
app.register_blueprint(search_bp, url_prefix='/api')

@app.route('/')
def home():
    return {
        'message': 'Task Forge API',
        'version': '1.0.0',
        'endpoints': {
            'GET /api/tasks': 'Obtener todas las tareas',
            'POST /api/tasks': 'Crear tarea/proyecto',
            'GET /api/tasks/<id>': 'Obtener tarea específica',
            'PUT /api/tasks/<id>': 'Actualizar tarea',
            'DELETE /api/tasks/<id>': 'Eliminar tarea',
            'GET /api/search?q=<query>': 'Buscar tareas'
        }
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)