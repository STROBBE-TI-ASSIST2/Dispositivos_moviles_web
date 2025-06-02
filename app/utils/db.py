from flask_sqlalchemy import SQLAlchemy
import urllib


import os
from dotenv import load_dotenv

load_dotenv()

# Leer credenciales desde el .env
server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
username = os.getenv("SQL_USER")
password = os.getenv("SQL_PASSWORD")

print("DEBUG:", server, database, username, password)  # Puedes borrar esto
# Codificar los parámetros para SQL Server
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password}"
)

# Crear la URI de conexión
db_uri = f"mssql+pyodbc:///?odbc_connect={params}"

# Crear instancia de SQLAlchemy sin pasar app (para usarla con init_app)
db = SQLAlchemy()

