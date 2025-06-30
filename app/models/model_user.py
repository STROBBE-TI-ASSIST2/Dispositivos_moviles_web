from app.utils.db import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = 'USUARIO'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)