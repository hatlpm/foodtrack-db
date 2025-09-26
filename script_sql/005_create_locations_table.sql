-- ============================================
-- SCRIPT: 005_create_locations_table.sql
-- DESCRIPCIÓN: Crear tabla de ubicaciones de foodtrucks
-- ============================================

USE FoodTrackBD;
--GO

CREATE TABLE locations (
    location_id INT IDENTITY(1,1) PRIMARY KEY,
    
    foodtruck_id INT NOT NULL,
    location_date DATE NOT NULL,
    zone NVARCHAR(100) NOT NULL,
    
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    
    CONSTRAINT FK_Location_Foodtruck FOREIGN KEY (foodtruck_id)
        REFERENCES foodtrucks(foodtruck_id)
);
--GO

-- Verificación
SELECT * FROM locations;
--GO