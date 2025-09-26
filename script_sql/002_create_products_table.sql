-- ============================================
-- SCRIPT: 003_create_orders_table.sql
-- DESCRIPCIÓN: Crear tabla de pedidos
-- ============================================

USE FoodTrackBD;

CREATE TABLE orders (
    order_id INT IDENTITY(1,1) PRIMARY KEY,
    
    foodtruck_id INT NOT NULL,
    
    order_date DATE NOT NULL,
    
    status NVARCHAR(50) NOT NULL 
        CHECK (status IN ('pendiente', 'entregado', 'cancelado')), 
        -- solo aceptamos valores válidos
    
    total DECIMAL(10,2) NOT NULL CHECK (total >= 0), 
    
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_Order_Foodtruck FOREIGN KEY (foodtruck_id)
        REFERENCES foodtrucks(foodtruck_id)
);

-- Verificar estructura
SELECT * FROM orders;
