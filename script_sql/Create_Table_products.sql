-- ============================================
-- SCRIPT: 002_create_products_table.sql
-- DESCRIPCIÓN: Crear tabla de productos
-- ============================================

USE FoodTrackBD;

CREATE TABLE products (
    product_id INT IDENTITY(1,1) PRIMARY KEY,
    
    -- Relación con foodtrucks
    foodtruck_id INT NOT NULL,
    
    name NVARCHAR(100) NOT NULL, -- Se refiere al producto son los platos
    price DECIMAL(10,2) NOT NULL,   -- hasta 10 dígitos, 2 decimales
    stock INT NOT NULL CHECK (stock >= 0), -- no puede haber stock negativo
    
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),

);
--GO

ALTER TABLE foodtrucks
-- Campos de auditoría (buena práctica) llevar registro de tiempo al momento de adicionar datos
ADD CONSTRAINT FK_Product_Foodtruck FOREIGN KEY (foodtruck_id)
        REFERENCES foodtrucks(foodtruck_id);

-- Verificación
SELECT * FROM products;
--GO