from flask import Blueprint, request, jsonify, session,render_template,redirect,url_for
from app.models.model_user import Usuario
from app.utils.db import db

auth_bp = Blueprint('auth', __name__)
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = Usuario.query.filter_by(username=username, password=password).first()
    if user:
        session['usuario'] = username

        return jsonify({'success': True, 'message': 'Welcome', 'redirect': url_for('menu.formulario')}), 200
    else:
        return jsonify({'success': False, 'message': 'Credenciales inválidas'}), 401

