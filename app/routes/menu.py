from flask import make_response, Blueprint, session,render_template,redirect,url_for
from flask_login import login_required, current_user

menu_bp = Blueprint('menu', __name__)
"""@menu_bp.route('/menu')
def formulario():
    if 'usuario' not in session:
        return redirect(url_for('auth.index'))  # Redirige a login si no hay sesión
    return render_template('MENU.html', usuario=session['usuario'])"""

@menu_bp.route('/menu')
@login_required
def menu():
    response = make_response(render_template('MENU.html', usuario=current_user.username))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response

    #return render_template('MENU.html', usuario=current_user.username)