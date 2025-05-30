from app.utils.db import db

class Usuario(db.Model):
    __tablename__ = 'USUARIO'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)