from flask import Blueprint, render_template, request, send_file
from app.models.mantenimento_pc import Mantenimiento_equipos
import pandas as pd
from io import BytesIO
import openpyxl
reportes = Blueprint('reportes', __name__)
#REDIRIGE A LA PANTALLA REPORTES DONDE GENERA EL EXCEL Y EL DASHBOARD
@reportes.route('/reportes', methods=['GET'])
def vista_reportes():
    columnas = [col.name for col in Mantenimiento_equipos.__table__.columns]
    return render_template('reportes.html', columnas=columnas)

@reportes.route('/reportes', methods=['POST'])
def generar_reporte():
    columnas = request.form.getlist('columnas')
    if not columnas:
        return "Selecciona al menos una columna", 400

    registros = Mantenimiento_equipos.query.with_entities(
        *[getattr(Mantenimiento_equipos, col) for col in columnas]
    ).all()

    df = pd.DataFrame(registros, columns=columnas)
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    return send_file(output, as_attachment=True, download_name='reporte_mantenimiento.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
