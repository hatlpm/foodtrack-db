-- Crear tabla foodtrucks
CREATE TABLE foodtrucks (
    -- IDENTITY(1,1) significa: empezar en 1, incrementar de 1 en 1
    -- PRIMARY KEY: esta columna identifica únicamente cada fila
    foodtruck_id INT IDENTITY(1,1) PRIMARY KEY,
    
    -- NVARCHAR: texto que soporta caracteres especiales (ñ, acentos)
    -- (100): máximo 100 caracteres
    -- NOT NULL: este campo es obligatorio
    name NVARCHAR(100) NOT NULL,
    
    -- Tipo de cocina
    cuisine_type NVARCHAR(50) NOT NULL,
    
    -- Ciudad donde opera
    city NVARCHAR(100) NOT NULL
);

-- Verificar que se creó correctamente
SELECT * FROM foodtrucks;

-- Agregar nuevas columnas

ALTER TABLE foodtrucks
-- Campos de auditoría (buena práctica) llevar registro de tiempo al momento de adicionar datos
ADD created_at DATETIME DEFAULT GETDATE(), updated_at DATETIME DEFAULT GETDATE();