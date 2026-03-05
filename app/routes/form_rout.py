from flask import Blueprint, request, jsonify, session,render_template,redirect,url_for
from db_schema.models_mantenimiento import Mantenimiento
from sqlalchemy import select
from flask import abort

from app import db
from flask_login import login_required

form_bp = Blueprint('form', __name__)

#Mostrar formulario
@form_bp.route('/formulario',methods=['GET'])
@login_required
def formulario():
    pc = request.args.get('id')
    return render_template('datos_pc.html', id=pc)

#Guardar los datos del formulario en la base de datos
@form_bp.route('/formulario', methods=['POST'])
def guardar_datos():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No se recibió JSON'}), 400

    # Validación para REPORTE Y ACCION CORRECTIVA
    reporte = data.get('reporte')
    accion_correctiva = data.get('accion_correctiva')
    if not reporte or not accion_correctiva:
        return jsonify({'success': False, 'message': 'Campos obligatorios faltantes'}), 400

    # Guardar en la base de datos
    nuevo = Mantenimiento(**data)
    db.session.add(nuevo)
    db.session.commit()

    return jsonify({'mensaje': 'Datos guardados correctamente'}), 200

#Consultar los datos del mantenimiento
@form_bp.route('/consulta-mantenimientos', methods=['GET'])
@login_required
def consulta_mantenimientos():
    registros = db.session.execute(
        select(Mantenimiento)
    ).scalars().all()
    return render_template('consulta_mante.html', registros=registros)

#metodo que envia los datos al front para verlos en los campos correspondientes
@form_bp.route('/api/mantenimientos/<int:id>', methods=['GET'])
def obtener_mantenimiento(id):
    #mantenimiento = Mantenimiento.query.get_or_404(id)
    mantenimiento = db.session.get(Mantenimiento, id) or abort(404)
    return jsonify({
        'id_pc': mantenimiento.id_pc,
        'codigo_stb': mantenimiento.codigo_stb,
        'nombre_equipo': mantenimiento.nombre_equipo,
        'ip': mantenimiento.ip,
        'sistema_operativo': mantenimiento.sistema_operativo,
        'procesador': mantenimiento.procesador,
        'ram': mantenimiento.ram,
        'office': mantenimiento.office,
        'reporte': mantenimiento.reporte,
        'accion_correctiva': mantenimiento.accion_correctiva

    })

#Metodo para actualizar
@form_bp.route('/api/mantenimientos/actualizar/<int:id>', methods=['PATCH'])
def api_actualizar_mantenimiento(id):
    mantenimiento = db.session.get(Mantenimiento, id) or abort(404)
    data = request.get_json()

    mantenimiento.codigo_stb = data.get('codigo_stb')
    mantenimiento.nombre_equipo = data.get('nombre_equipo')
    mantenimiento.ip = data.get('ip')
    mantenimiento.sistema_operativo = data.get('sistema_operativo')
    mantenimiento.procesador = data.get('procesador')
    mantenimiento.ram = data.get('ram')
    mantenimiento.office = data.get('office')
    mantenimiento.reporte = data.get('reporte')
    mantenimiento.accion_correctiva = data.get('accion_correctiva')

    db.session.commit()
    return jsonify({'message': 'Mantenimiento actualizado correctamente'})

@form_bp.route('/api/mantenimientos/<int:id>', methods=['DELETE'])
@login_required
def eliminar_mantenimiento(id):
    mantenimiento = db.session.get(Mantenimiento, id) or abort(404)
    db.session.delete(mantenimiento)
    db.session.commit()
    return jsonify({'message': 'Mantenimiento eliminado correctamente'})

##########################
