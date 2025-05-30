from app import db

class Mantenimiento_equipos(db.Model):
    __tablename__ = 'Mantenimientos_pc'
    id_pc = db.Column(db.Integer, primary_key=True)
    codigo_stb = db.Column(db.String(15), nullable=False)
    nombre_equipo = db.Column(db.String(20), nullable=False)
    ip = db.Column(db.String(20), nullable=False)
    sistema_operativo = db.Column(db.String(30), nullable=False)
    procesador = db.Column(db.String(10), nullable=False)
    ram = db.Column(db.Integer, nullable=False)
    office = db.Column(db.String(20), nullable=False)
    reporte = db.Column(db.String(100), nullable=False)
    accion_correctiva = db.Column(db.String(100), nullable=False)

