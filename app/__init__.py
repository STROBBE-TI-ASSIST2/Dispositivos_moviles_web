import importlib
import pkgutil
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from pathlib import Path
import db_schema  # >>> para ubicar la carpeta de migraciones del paquete

from app.utils.db import db, db_uri
from db_schema.models_generales import Usuario  # >>> modelo desde el paquete
from db_schema.models_generales import Usuario
from db_schema.models_mantenimiento import Usuario_mantto

login_manager = LoginManager()
login_manager.login_view = 'main.index'

#Fncion que me muestra todos modelos de db_schema
def _import_all_db_schema_models():
    # carga todo excepto el paquete de migraciones
    for _, name, _ in pkgutil.walk_packages(db_schema.__path__, db_schema.__name__ + "."):
        if ".migrations" in name:
            continue
        importlib.import_module(name)

def create_app():
    from app.routes.auth_rout import main_bp, auth_bp
    from app.routes.form_rout import form_bp
    from app.routes.menu import menu_bp
    from app.routes.reportes_rout import reportes

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'clave-secreta'

    db.init_app(app)

    # >>> Fuerza import de modelos del paquete para que Alembic “los vea”
    #import db_schema.models_tickets.usuario
    #import db_schema.models_tickets.mantenimiento  # si lo usas

    _import_all_db_schema_models()

    # >>> Muy importante: apuntar Migrate al repo de migraciones del paquete
    MIGRATIONS_DIR = Path(db_schema.__file__).parent / "migrations"
    Migrate(app, db, directory=str(MIGRATIONS_DIR))
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # >>> En SQLAlchemy 2.x es mejor usar session.get
        return db.session.get(Usuario_mantto, int(user_id))

    # >>> Quita create_all(): usarás migraciones (upgrade), no create_all()
    # with app.app_context():
    #     db.create_all()

    # Registrar rutas
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(form_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(reportes)
    return app
