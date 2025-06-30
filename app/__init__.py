from flask import Flask
from flask_migrate import Migrate
from app.utils.db import db, db_uri
from flask_login import LoginManager
from app.models.model_user import Usuario

login_manager = LoginManager()
login_manager.login_view = 'main.index'

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
    migrate = Migrate(app, db)
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))


    with app.app_context():
        db.create_all()

    # Registrar rutas

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(form_bp)
    app.register_blueprint(menu_bp)

    return app


