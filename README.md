# 🍔 FoodTrack Database Project

## ✨ Descripción del Proyecto

Este proyecto implementa el esquema relacional inicial para **FoodTrack**, una plataforma diseñada para gestionar las operaciones de foodtrucks en distintas ubicaciones de una ciudad. El objetivo es simular un entorno de desarrollo profesional, utilizando **Microsoft SQL Server** como motor de base de datos, **DBeaver** como cliente de gestión, y **Git/GitHub** para el control de versiones.

La base de datos contempla la información esencial de:
-   **Foodtrucks**: Detalles de cada negocio.
-   **Productos**: Ítems ofrecidos por cada foodtruck.
-   **Pedidos (Orders)**: Transacciones de los clientes.
-   **Ítems de Pedido (Order Items)**: Detalle de los productos en cada pedido.
-   **Ubicaciones (Locations)**: Registro de dónde operan los foodtrucks.

## 🛠️ Tecnologías Utilizadas

*   **Motor de Base de Datos**: Microsoft SQL Server
*   **Cliente de Base de Datos**: DBeaver
*   **Control de Versiones**: Git & GitHub
*   **Lenguaje de Consulta**: SQL

## 📂 Estructura del Proyecto

El repositorio está organizado de la siguiente manera:

```
/FoodTrackDB
├── /scripts/
│ ├── 001_create_foodtrucks_table.sql
│ ├── 002_create_products_table.sql
│ ├── 003_create_orders_table.sql
│ ├── 004_create_order_items_table.sql
│ └── 005_create_locations_table.sql
├── /data/
│ ├── foodtrucks.csv
│ ├── products.csv
│ ├── orders.csv
│ ├── order_items.csv
│ └── locations.csv
└── README.md
```

## 🚀 Instalación y Configuración

Para configurar el entorno y la base de datos, sigue estos pasos:

1. **Clonar el Repositorio:**

    ```
    git clone https://github.com/tu-usuario/FoodTrackDB.git
    cd FoodTrackDB
    ```


2. **Instalar SQL Server:**

    Asegúrate de tener una instancia de Microsoft SQL Server instalada y en funcionamiento. Puedes descargar la edición Developer o Express desde el sitio oficial de Microsoft.

3. **Instalar DBeaver:**
    Descarga e instala DBeaver (Community Edition)  desde dbeaver.io.

4. **Conectar DBeaver a SQL Server:**
    * Abre DBeaver.
   * Crea una nueva conexión de base de datos (File -> New -> Database Connection).
   * Selecciona "SQL Server" y sigue los pasos para conectar a tu instancia local.

5. **Crear la Base de Datos FoodTrackDB:**
    En DBeaver, abre una nueva ventana de script SQL y ejecuta:

    ```CREATE DATABASE FoodTrackDB; GO```

## 📝 Uso

   **Creación de Tablas**
   1. Abre DBeaver y conéctate a la base de datos FoodTrackDB que creaste.
   2. Navega a la carpeta /scripts en tu repositorio clonado.
   3. Ejecuta los scripts SQL en el siguiente orden para crear las tablas y sus relaciones:
   * ```001_create_foodtrucks_table.sql```
   * ```002_create_products_table.sql```
   * ```003_create_orders_table.sql```
   * ```004_create_order_items_table.sql```
   * ```005_create_locations_table.sql```
   Puedes abrir cada archivo en DBeaver y ejecutarlo, o concatenarlos en un solo script maestro si lo prefieres.