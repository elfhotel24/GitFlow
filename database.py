import pyodbc
from config import DATABASE_CONFIG

class Database:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            connection_string = (
                f"DRIVER={DATABASE_CONFIG['DRIVER']};"
                f"SERVER={DATABASE_CONFIG['SERVER']};"
                f"DATABASE={DATABASE_CONFIG['DATABASE']};"
                f"Trusted_Connection={DATABASE_CONFIG['Trusted_Connection']};"
            )
            self.connection = pyodbc.connect(connection_string)
            print("✅ Conexión a SQL Server exitosa!")
        except Exception as e:
            print(f"❌ Error conectando a la base de datos: {e}")
    
    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor
        except Exception as e:
            print(f"Error ejecutando query: {e}")
            return None
    
    def fetch_all(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    def fetch_one(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching single record: {e}")
            return None