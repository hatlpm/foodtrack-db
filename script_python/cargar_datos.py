import pyodbc
import pandas as pd
from datetime import datetime
import sys
import os

class FoodTrackLoader:
    def __init__(self, server, database, username=None, password=None):
        """
        Inicializar conexión a SQL Server
        
        Args:
            server: Nombre del servidor (ej: 'localhost' o 'DESKTOP-ABC123\\SQLEXPRESS')
            database: Nombre de la base de datos
            username: Usuario (opcional, si usas SQL Auth)
            password: Contraseña (opcional, si usas SQL Auth)
        """
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = None
        
    def conectar(self):
        """Establecer conexión con SQL Server"""
        try:
            if self.username and self.password:
                # Autenticación SQL Server
                connection_string = f"""
                DRIVER={{ODBC Driver 17 for SQL Server}};
                SERVER={self.server};
                DATABASE={self.database};
                UID={self.username};
                PWD={self.password};
                """
            else:
                # Autenticación Windows (Trusted Connection)
                connection_string = f"""
                DRIVER={{ODBC Driver 17 for SQL Server}};
                SERVER={self.server};
                DATABASE={self.database};
                Trusted_Connection=yes;
                """
            
            self.connection = pyodbc.connect(connection_string)
            print(f"✅ Conexión exitosa a {self.database}")
            return True
            
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False
    
    def crear_tabla_errores(self):
        """Crear tabla para registrar errores de inserción"""
        try:
            cursor = self.connection.cursor()
            
            # Crear tabla failed_orders si no existe
            sql_create_failed = """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='failed_orders' AND xtype='U')
            CREATE TABLE failed_orders (
                error_id INT IDENTITY(1,1) PRIMARY KEY,
                tabla_destino NVARCHAR(50) NOT NULL,
                registro_fallido NVARCHAR(MAX),
                error_mensaje NVARCHAR(MAX),
                fecha_error DATETIME DEFAULT GETDATE()
            );
            """
            
            cursor.execute(sql_create_failed)
            self.connection.commit()
            print("✅ Tabla 'failed_orders' verificada/creada")
            
        except Exception as e:
            print(f"❌ Error creando tabla de errores: {e}")
    
    def registrar_error(self, tabla, registro, error):
        """Registrar error en la tabla failed_orders"""
        try:
            cursor = self.connection.cursor()
            
            sql_insert_error = """
            INSERT INTO failed_orders (tabla_destino, registro_fallido, error_mensaje)
            VALUES (?, ?, ?)
            """
            
            cursor.execute(sql_insert_error, tabla, str(registro), str(error))
            self.connection.commit()
            print(f"⚠️ Error registrado para tabla {tabla}")
            
        except Exception as e:
            print(f"❌ Error registrando error: {e}")
    
    def cargar_foodtrucks(self, csv_path):
        """Cargar datos de foodtrucks desde CSV"""
        try:
            # Leer CSV
            df = pd.read_csv(csv_path)
            print(f"📁 Leyendo {len(df)} registros de {csv_path}")
            
            cursor = self.connection.cursor()
            exitosos = 0
            errores = 0
            
            for index, row in df.iterrows():
                try:
                    # Insertar registro (sin foodtruck_id porque es IDENTITY)
                    sql_insert = """
                    INSERT INTO foodtrucks (name, cuisine_type, city)
                    VALUES (?, ?, ?)
                    """
                    
                    cursor.execute(sql_insert, 
                                 row['name'], 
                                 row['cuisine_type'], 
                                 row['city'])
                    
                    exitosos += 1
                    
                except Exception as e:
                    errores += 1
                    self.registrar_error('foodtrucks', row.to_dict(), e)
            
            # Confirmar transacción
            self.connection.commit()
            
            print(f"✅ Foodtrucks cargados: {exitosos} exitosos, {errores} errores")
            return exitosos, errores
            
        except Exception as e:
            print(f"❌ Error general cargando foodtrucks: {e}")
            return 0, 0
    
    def cargar_products(self, csv_path):
        """Cargar datos de productos desde CSV"""
        try:
            df = pd.read_csv(csv_path)
            print(f"📁 Leyendo {len(df)} registros de {csv_path}")
            
            cursor = self.connection.cursor()
            exitosos = 0
            errores = 0
            
            for index, row in df.iterrows():
                try:
                    sql_insert = """
                    INSERT INTO products (foodtruck_id, name, price, stock)
                    VALUES (?, ?, ?, ?)
                    """
                    
                    cursor.execute(sql_insert,
                                 row['foodtruck_id'],
                                 row['name'],
                                 row['price'],
                                 row['stock'])
                    
                    exitosos += 1
                    
                except Exception as e:
                    errores += 1
                    self.registrar_error('products', row.to_dict(), e)
            
            self.connection.commit()
            print(f"✅ Productos cargados: {exitosos} exitosos, {errores} errores")
            return exitosos, errores
            
        except Exception as e:
            print(f"❌ Error general cargando productos: {e}")
            return 0, 0
    
    def cargar_orders(self, csv_path):
        """Cargar datos de pedidos desde CSV"""
        try:
            df = pd.read_csv(csv_path)
            print(f"📁 Leyendo {len(df)} registros de {csv_path}")
            
            cursor = self.connection.cursor()
            exitosos = 0
            errores = 0
            
            for index, row in df.iterrows():
                try:
                    sql_insert = """
                    INSERT INTO orders (foodtruck_id, order_date, status, total)
                    VALUES (?, ?, ?, ?)
                    """
                    
                    cursor.execute(sql_insert,
                                 row['foodtruck_id'],
                                 row['order_date'],
                                 row['status'],
                                 row['total'])
                    
                    exitosos += 1
                    
                except Exception as e:
                    errores += 1
                    self.registrar_error('orders', row.to_dict(), e)
            
            self.connection.commit()
            print(f"✅ Pedidos cargados: {exitosos} exitosos, {errores} errores")
            return exitosos, errores
            
        except Exception as e:
            print(f"❌ Error general cargando pedidos: {e}")
            return 0, 0
    
    def verificar_carga(self):
        """Verificar conteos después de la carga"""
        try:
            cursor = self.connection.cursor()
            
            tablas = ['foodtrucks', 'products', 'orders', 'order_items', 'locations']
            
            print("\n📊 RESUMEN DE CARGA:")
            print("-" * 30)
            
            for tabla in tablas:
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                print(f"{tabla}: {count} registros")
            
            # Mostrar errores si los hay
            cursor.execute("SELECT COUNT(*) FROM failed_orders")
            errores_total = cursor.fetchone()[0]
            
            if errores_total > 0:
                print(f"\n⚠️ Total de errores registrados: {errores_total}")
                cursor.execute("SELECT TOP 5 * FROM failed_orders ORDER BY fecha_error DESC")
                print("Últimos 5 errores:")
                for row in cursor.fetchall():
                    print(f"  - {row[1]}: {row[3][:100]}...")
            else:
                print("\n✅ No hay errores registrados")
                
        except Exception as e:
            print(f"❌ Error verificando carga: {e}")
    
    def cerrar_conexion(self):
        """Cerrar conexión"""
        if self.connection:
            self.connection.close()
            print("🔌 Conexión cerrada")

# ============================================
# FUNCIÓN PRINCIPAL
# ============================================
def main():
    """Función principal para ejecutar la carga"""
    
    # CONFIGURACIÓN - AJUSTA ESTOS VALORES
    SERVER = "localhost"  # o "DESKTOP-ABC123\\SQLEXPRESS"
    DATABASE = "FoodTrackBD"
    
    # Si usas autenticación SQL Server, descomenta y completa:
    # USERNAME = "tu_usuario"
    # PASSWORD = "tu_password"
    
    # Rutas de los archivos CSV
    CSV_FOLDER = "data_csv"  # Ajusta la ruta donde tienes tus CSV
    
    # Crear instancia del loader
    loader = FoodTrackLoader(SERVER, DATABASE)
    
    try:
        # Conectar
        if not loader.conectar():
            print("❌ No se pudo conectar. Verifica la configuración.")
            return
        
        # Crear tabla de errores
        loader.crear_tabla_errores()
        
        print("\n🚀 INICIANDO CARGA DE DATOS...")
        print("=" * 40)
        
        # Cargar datos en orden (respetando FKs)
        if os.path.exists(f"{CSV_FOLDER}/foodtrucks.csv"):
            loader.cargar_foodtrucks(f"{CSV_FOLDER}/foodtrucks.csv")
        
        if os.path.exists(f"{CSV_FOLDER}/products.csv"):
            loader.cargar_products(f"{CSV_FOLDER}/products.csv")
        
        if os.path.exists(f"{CSV_FOLDER}/orders.csv"):
            loader.cargar_orders(f"{CSV_FOLDER}/orders.csv")
        
        # Verificar resultados
        loader.verificar_carga()
        
        print("\n🎉 CARGA COMPLETADA")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
    
    finally:
        loader.cerrar_conexion()

if __name__ == "__main__":
    main()