from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import urllib
import pyodbc

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

"""
# Datos de conexión
# Configura los datos de tu servidor SQL
SQL_SERVER = 'serverp01'            # Ej: 'localhost' o '192.168.1.100'
SQL_DATABASE = 'STROBBE_APPS'     # Ej: 'mantenimientos'
SQL_USER = '1administ22'               # Ej: 'sa'
SQL_PASSWORD = '2024.SISTEM'        # Ej: '1234'

params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SQL_SERVER};"
    f"DATABASE={SQL_DATABASE};"
    f"UID={SQL_USER};"
    f"PWD={SQL_PASSWORD}"
)

# URI de conexión
DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"

# SQLAlchemy instance
db = SQLAlchemy()"""