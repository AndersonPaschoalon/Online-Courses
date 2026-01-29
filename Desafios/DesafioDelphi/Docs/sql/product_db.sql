CREATE DATABASE product_db;

\c product_db;

CREATE TABLE Product (
    id SERIAL PRIMARY KEY,        -- Chave primária auto-incrementável
    Name VARCHAR(255) NOT NULL,   -- Nome do produto
    Price DOUBLE PRECISION NOT NULL,  -- Preço do produto
    Description TEXT,             -- Descrição do produto
    Manufacturer VARCHAR(255)     -- Fabricante do produto
);

INSERT INTO Product (Name, Price, Description, Manufacturer)
VALUES
    ('Abacate', 1.99, 'Fruta', 'Fazenda Ametista'),
    ('Banana', 0.99, 'Fruta', 'Fazenda Barranco'),
    ('Carambola', 2.49, 'Fruta', 'Fazenda Cavalo'),
    ('Damasco', 3.79, 'Fruta', 'Fazenda Da Avó'),
    ('Espinafre', 1.49, 'Verdura', 'Fazenda Esmeralda'),
    ('Goiaba', 2.19, 'Fruta', 'Fazenda Goiás');

SELECT * FROM Product;
