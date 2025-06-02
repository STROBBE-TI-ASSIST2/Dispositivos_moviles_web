from flask import Blueprint, request, jsonify, session,render_template,redirect,url_for
from app.models.mantenimento_pc import Mantenimiento_equipos
from app import db

form_bp = Blueprint('form', __name__)

'''@form_bp.route('/formulario')
def formulario():
    if 'usuario' not in session:
        return redirect(url_for('auth.index'))  # Redirige a login si no hay sesión
    return render_template('datos_pc.html', usuario=session['usuario'])'''

#Mostrar formulario
@form_bp.route('/formulario')
def formulario():
    return render_template('datos_pc.html')

#Guardar los datos del formulario en la base de datos
@form_bp.route('/formulario', methods=['POST'])
def guardar_datos():
    if 'usuario' not in session:
        return redirect(url_for('auth.index'))

    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No se recibió JSON'}), 400

    codigo_stb = data.get('codigo_stb')
    nombre_equipo = data.get('nombre_equipo')
    ip = data.get('ip')
    sistema_operativo = data.get('sistema_operativo')
    procesador = data.get('procesador')
    ram = data.get('ram')
    office = data.get('office')
    reporte = data.get('reporte')
    accion_correctiva = data.get('accion_correctiva')

    # Validaciones básicas
    if not reporte or not accion_correctiva:
        return jsonify({'success': False, 'message': 'Campos obligatorios faltantes'}), 400



    # Guardar en la base de datos
    nuevo = Mantenimiento_equipos(codigo_stb=codigo_stb, nombre_equipo=nombre_equipo,
                                  ip=ip, sistema_operativo= sistema_operativo,
                                  procesador=procesador, ram=ram,
                                  office= office, reporte=reporte,
                                  accion_correctiva=accion_correctiva
                                  )
    db.session.add(nuevo)
    db.session.commit()

    return jsonify({'mensaje': 'Datos guardados correctamente'}), 200

#Consultar los datos del mantenimiento
@form_bp.route('/consulta-mantenimientos', methods=['GET'])
def consulta_mantenimientos():
    registros = Mantenimiento_equipos.query.all()
    return render_template('consulta_mante.html', registros=registros)