# 🐍 Explicación COMPLETA del código Python
## 📋 1. Importación de librerías

```
import pyodbc
import pandas as pd
```

¿Qué hace ``import``?

``import`` le dice a Python: "quiero usar funciones de esta librería externa"
Es como decir "necesito estas herramientas para trabajar"

¿Qué es pyodbc?

* py = Python
* odbc = Open Database Connectivity (estándar para conectarse a bases de datos)
* Te permite conectar Python con SQL Server, MySQL, Oracle, etc.
* Sin esto, Python no sabría cómo "hablar" con SQL Server
  
## 📋 2. Variables de configuración
```
servidor = "localhost"
base_datos = "FoodTrackDB"
```

¿Por qué variables?

* En lugar de escribir "localhost" en 10 lugares diferentes, lo pones en UNA variable
* Si cambias de servidor, solo modificas UNA línea
* Es una buena práctica de programación

¿Qué es localhost?

* Significa "mi propia computadora"
* Es lo mismo que decir 127.0.0.1 (dirección IP local)
* Si tu SQL Server estuviera en otra máquina, pondrías su IP o nombre


## 📋 3. Bloque try-except para conexión
```
print("🔌 Conectando a SQL Server...")

try:
    conexion = pyodbc.connect(f"""
        DRIVER={{ODBC Driver 17 for SQL Server}};
        SERVER={servidor};
        DATABASE={base_datos};
        Trusted_Connection=yes;
    """)
    
    print("✅ ¡Conectado exitosamente!")
    
except Exception as error:
    print(f"❌ Error de conexión: {error}")
    exit()
```

¿Qué es print()?

* Muestra texto en la pantalla/consola
* Los emojis (🔌 ✅ ❌) son solo para que se vea bonito y claro

¿Qué es try-except?
* try: "Intenta hacer esto"
* except: "Si algo sale mal, haz esto otro"
* Es como decir: "Intenta conectarte, pero si falla, no crashes el programa"

¿Qué es pyodbc.connect()?

* Función que establece la conexión con la base de datos
* Le pasas un "string de conexión" con todos los parámetros

¿Qué significa cada parámetro del string de conexión?

```
f"""
DRIVER={{ODBC Driver 17 for SQL Server}};
SERVER={servidor};
DATABASE={base_datos};
Trusted_Connection=yes;
"""
```

* f""": Es un "f-string" → permite meter variables dentro con {variable}
* DRIVER: Le dice qué "traductor" usar para hablar con SQL Server
* SERVER: La dirección del servidor (localhost = tu PC)
* DATABASE: El nombre de la base de datos específica
* Trusted_Connection=yes: Usa tu usuario de Windows (no pide usuario/contraseña)
* {{ y }}: Se escriben dobles porque dentro de f-strings, las llaves simples {} son especiales
¿Qué es exit()?
Termina el programa inmediatamente
Si no se puede conectar a la base, no tiene sentido continuar

## 📋 4. Crear cursor y tabla de errores
```
cursor = conexion.cursor()

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

```

¿Qué es un cursor?
* Es como un "puntero" o "control remoto" para ejecutar comandos SQL
* La conexión es el "cable", el cursor es el "control remoto"
* Con el cursor puedes hacer SELECT, INSERT, UPDATE, etc.

¿Qué hace """ (triple comillas)?

* Permite escribir texto en múltiples líneas
* Perfecto para comandos SQL largos
* Sin las triple comillas tendrías que escribir todo en una línea

¿Qué hace este SQL?
```
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='failed_orders' AND xtype='U')
CREATE TABLE failed_orders (...)
```

* IF NOT EXISTS: "Si no existe esta tabla..."
* sysobjects: Tabla del sistema que lista todos los objetos (tablas, vistas, etc.)
* xtype='U': Tipo 'U' = User table (tabla de usuario)
* CREATE TABLE: Crea la tabla solo si no existe

¿Qué es cursor.execute()?
* Ejecuta el comando SQL que le pases
* Es como presionar "Execute" en DBeaver, pero desde Python

¿Qué es conexion.commit()?
* Confirma los cambios en la base de datos
* Sin commit(), los cambios quedan "pendientes" y se pueden perder
* Es como "Guardar" en Word

## 📋 5. Lectura del CSV con pandas

```
try:
    df_foodtrucks = pd.read_csv("foodtrucks.csv")
    print(f"📁 Archivo leído: {len(df_foodtrucks)} registros")
```
¿Qué es pd.read_csv()?

* Función de pandas que lee archivos CSV
* Convierte el CSV en un "DataFrame" (tabla en memoria de Python)
* Automáticamente detecta columnas, tipos de datos, etc.

¿Qué es un DataFrame?

* Es como una tabla de Excel dentro de Python
* Tiene filas y columnas
* Puedes hacer df['columna'] para acceder a una columna específica

¿Qué hace len(df_foodtrucks)?

* len() = length = longitud
* Te dice cuántas filas tiene el DataFrame
* Es como contar cuántos registros hay en el CSV

## 📋 6. Loop para insertar fila por fila
```
exitosos = 0
errores = 0

for index, fila in df_foodtrucks.iterrows():
    try:
        sql_insertar = """
        INSERT INTO foodtrucks (name, cuisine_type, city)
        VALUES (?, ?, ?)
        """
        
        cursor.execute(sql_insertar, 
                     fila['name'], 
                     fila['cuisine_type'], 
                     fila['city'])
        
        exitosos += 1
        print(f"  ✅ Insertado: {fila['name']}")
        
    except Exception as error:
        errores += 1
        print(f"  ❌ Error con: {fila['name']} - {error}")

```

¿Qué son las variables exitosos y errores?

* Contadores para llevar estadísticas
* Empiezan en 0 y van sumando 1 cada vez que algo pasa bien o mal

¿Qué es for index, fila in df_foodtrucks.iterrows()?

* for: Repite algo para cada elemento de una lista
* iterrows(): Función de pandas que va fila por fila del DataFrame
* index: El número de fila (0, 1, 2, 3...)
fila: Los datos de esa fila específica

Es como decir: "Para cada fila del CSV, haz esto..."

¿Qué son los ? en el SQL?

```
INSERT INTO foodtrucks (name, cuisine_type, city)
VALUES (?, ?, ?)
```

* Son marcadores de parámetros
* Evitan "SQL Injection" (ataques de seguridad)
pyodbc reemplaza cada ? con el valor correspondiente de forma segura

¿Qué hace fila['name']?
* Accede a la columna name de esa fila específica
* Es como decir "dame el valor de la columna 'name' en esta fila"

¿Qué hace exitosos += 1?
* Es lo mismo que exitosos = exitosos + 1
* Suma 1 al contador de registros exitosos

## 📋 7. Verificación de resultados
```
cursor.execute("SELECT COUNT(*) FROM foodtrucks")
total_foodtrucks = cursor.fetchone()[0]
print(f"Total foodtrucks en base: {total_foodtrucks}")
```

¿Qué hace SELECT COUNT(*)?
* Cuenta cuántas filas hay en la tabla foodtrucks
* COUNT(*) = "cuenta todas las filas"

¿Qué es fetchone()?
* Obtiene una sola fila del resultado de la consulta
* COUNT(*) siempre devuelve una sola fila con un número
* 
¿Qué significa [0]?

* fetchone() devuelve una tupla (lista inmutable)
* [0] toma el primer (y único) elemento de esa tupla
* Es el número que devolvió COUNT(*)

## 📋 8. Mostrar registros

```
cursor.execute("SELECT TOP 3 * FROM foodtrucks ORDER BY foodtruck_id DESC")
for fila in cursor.fetchall():
    print(f"  ID: {fila[0]}, Nombre: {fila[1]}, Tipo: {fila[2]}")
```

¿Qué hace SELECT TOP 3 * ... ORDER BY ... DESC?
* TOP 3: Solo los primeros 3 registros
* *: Todas las columnas
* ORDER BY foodtruck_id DESC: Ordenados por ID de mayor a menor (los más recientes primero)

¿Qué es fetchall()?
* Obtiene todas las filas del resultado
* A diferencia de fetchone() que trae solo una

¿Qué significa fila[0], fila[1], fila[2]?
* Cada fila es una tupla con los valores de las columnas
* [0] = primera columna (foodtruck_id)
* [1] = segunda columna (name)
* [2] = tercera columna (cuisine_type)

## 📋 9. Cerrar conexión
```
conexion.close()
print("🔌 Conexión cerrada")
```

¿Por qué cerrar la conexión?
Las conexiones a bases de datos consumen recursos
Es una buena práctica cerrarlas cuando terminas
Evita problemas de "demasiadas conexiones abiertas"