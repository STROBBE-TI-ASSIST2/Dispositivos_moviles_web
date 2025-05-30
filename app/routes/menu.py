from flask import Blueprint, request, jsonify, session,render_template,redirect,url_for, flash
from app.models.mantenimento_pc import Mantenimiento_equipos
from app import db

menu_bp = Blueprint('menu', __name__)
@menu_bp.route('/menu')
def formulario():
    if 'usuario' not in session:
        return redirect(url_for('auth.index'))  # Redirige a login si no hay sesión
    return render_template('MENU.html', usuario=session['usuario'])