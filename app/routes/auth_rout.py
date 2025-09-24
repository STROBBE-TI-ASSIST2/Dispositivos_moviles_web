from flask import make_response, Blueprint, request, jsonify, session,render_template,url_for, redirect
from flask_login import login_user, logout_user, current_user
from db_schema.models_generales import Usuario
from db_schema.models_mantenimiento import Mantenimiento

from sqlalchemy import select
from app.utils.db import db




auth_bp = Blueprint('auth', __name__)
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('menu.menu'))

    response = make_response(render_template('index.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response


"""@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = Usuario.query.filter_by(username=username, password=password).first()
    if user:
        session['usuario'] = username

        return jsonify({'success': True, 'message': 'Welcome', 'redirect': url_for('menu.formulario')}), 200
    else:
        return jsonify({'success': False, 'message': 'Credenciales inválidas'}), 401"""


@auth_bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        #user = Usuario.query.filter_by(username=username).first()
        user = db.session.execute(
            select(Usuario).where(Usuario.username == username)
        ).scalar_one_or_none()
        if user and user.password == password:
            login_user(user)
            return jsonify({'success': True, 'message': 'Welcome', 'redirect': url_for('menu.menu')}), 200
        else:
            return jsonify({'success': False, 'message': 'Credenciales inválidas'}), 401



@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
