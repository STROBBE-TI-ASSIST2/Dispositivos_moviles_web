from flask import Flask, render_template, request, jsonify, redirect, session, url_for
import sqlite3
from flask_migrate import Migrate
import sqlite3
from app.utils.db import db, db_uri


def create_app():

    from app.routes.auth_rout import main_bp
    from app.routes.auth_rout import auth_bp
    from app.routes.form_rout import form_bp
    from app.routes.menu import menu_bp
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'clave-secreta'

    db.init_app(app)

    # Importar modelos antes de crear las tablas
    from app.models import model_user
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    # Registrar rutas

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(form_bp)
    app.register_blueprint(menu_bp)


    return app
