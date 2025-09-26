-- ============================================
-- SCRIPT: 004_create_order_items_table.sql
-- DESCRIPCIÓN: Crear tabla de ítems de pedidos
-- ============================================

USE FoodTrackBD;
--GO

CREATE TABLE order_items (
    order_item_id INT IDENTITY(1,1) PRIMARY KEY,
    
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    
    quantity INT NOT NULL CHECK (quantity > 0),
    
    -- Guardamos el precio unitario en el momento del pedido
    unit_price DECIMAL(10,2) NOT NULL,  
    
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    
    -- Foreign Keys
    CONSTRAINT FK_OrderItem_Order FOREIGN KEY (order_id)
        REFERENCES orders(order_id),
    
    CONSTRAINT FK_OrderItem_Product FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);
--GO

-- Verificar
SELECT * FROM order_items;
--GO