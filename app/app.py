from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from .db.db import db 
from .routes.empleado_routes import empleado_bp
from .controllers.gestor_db_empleados import gestor_db_empleados

load_dotenv()
app = Flask(__name__)
CORS(app, origins=["*"], supports_credentials=True)
try:
    db.connect()
    gestor_db_empleados.inicializar_coleccion()
except Exception as e:
    print(f"ERROR: No se pudo conectar a MongoDB. {e}")

app.register_blueprint(empleado_bp)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'PeopleFlow▶Backend activo y funcionando.',
        'status': 'active'
    }), 200