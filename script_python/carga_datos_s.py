import pyodbc
import pandas as pd

# ============================================
# CONFIGURACIÓN (CAMBIA ESTOS VALORES)
# ============================================
servidor = "localhost"  # Tu servidor SQL Server
base_datos = "FoodTrackBD"  # Tu base de datos

# ============================================
# 1. CONECTAR A SQL SERVER
# ============================================
print("🔌 Conectando a SQL Server...")

try:
    # Crear conexión (Windows Authentication)
    conexion = pyodbc.connect(f"""
        DRIVER={{ODBC Driver 17 for SQL Server}};
        SERVER={servidor};
        DATABASE={base_datos};
        Trusted_Connection=yes;
    """)
    
    print("✅ ¡Conectado exitosamente!")
    
except Exception as error:
    print(f"❌ Error de conexión: {error}")
    exit()  # Salir si no se puede conectar

# ============================================
# 2. CREAR TABLA DE ERRORES
# ============================================
print("📋 Creando tabla de errores...")

cursor = conexion.cursor()

# SQL para crear tabla de errores
sql_tabla_errores = """
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='failed_orders' AND xtype='U')
CREATE TABLE failed_orders (
    error_id INT IDENTITY(1,1) PRIMARY KEY,
    tabla_destino NVARCHAR(50),
    error_mensaje NVARCHAR(500),
    fecha_error DATETIME DEFAULT GETDATE()
);
"""

cursor.execute(sql_tabla_errores)
conexion.commit()
print("✅ Tabla de errores lista")

# ============================================
# 3. CARGAR FOODTRUCKS
# ============================================
print("🚚 Cargando foodtrucks...")

# Leer archivo CSV
try:
    df_foodtrucks = pd.read_csv("data_csv/foodtrucks.csv")
    print(f"📁 Archivo leído: {len(df_foodtrucks)} registros")
    
    # Insertar cada fila
    exitosos = 0
    errores = 0
    
    for index, fila in df_foodtrucks.iterrows():
        try:
            # SQL para insertar (sin foodtruck_id porque es automático)
            sql_insertar = """
            INSERT INTO foodtrucks (name, cuisine_type, city)
            VALUES (?, ?, ?)
            """
            
            # Ejecutar inserción
            cursor.execute(sql_insertar, 
                         fila['name'], 
                         fila['cuisine_type'], 
                         fila['city'])
            
            exitosos += 1
            print(f"  ✅ Insertado: {fila['name']}")
            
        except Exception as error:
            errores += 1
            print(f"  ❌ Error con: {fila['name']} - {error}")
            
            # Guardar error en tabla
            cursor.execute("""
                INSERT INTO failed_orders (tabla_destino, error_mensaje)
                VALUES ('foodtrucks', ?)
            """, str(error))
    
    # Confirmar cambios
    conexion.commit()
    print(f"🎉 Foodtrucks: {exitosos} exitosos, {errores} errores")
    
except Exception as error:
    print(f"❌ Error leyendo CSV: {error}")

# ============================================
# 4. VERIFICAR RESULTADOS
# ============================================
print("📊 Verificando resultados...")

# Contar registros en foodtrucks
cursor.execute("SELECT COUNT(*) FROM foodtrucks")
total_foodtrucks = cursor.fetchone()[0]
print(f"Total foodtrucks en base: {total_foodtrucks}")

# Contar errores
cursor.execute("SELECT COUNT(*) FROM failed_orders")
total_errores = cursor.fetchone()[0]
print(f"Total errores registrados: {total_errores}")

# Mostrar algunos registros
print("\n📋 Últimos foodtrucks insertados:")
cursor.execute("SELECT TOP 3 * FROM foodtrucks ORDER BY foodtruck_id DESC")
for fila in cursor.fetchall():
    print(f"  ID: {fila[0]}, Nombre: {fila[1]}, Tipo: {fila[2]}")

# ============================================
# 5. CERRAR CONEXIÓN
# ============================================
conexion.close()
print("🔌 Conexión cerrada")
print("✅ ¡Proceso completado!")