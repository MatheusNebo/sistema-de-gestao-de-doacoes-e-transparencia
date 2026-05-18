-- Seed data para teste das tabelas do sistema
BEGIN;

-- DONORS
WITH donor_pf AS (
    INSERT INTO donor (donor_type, name, cpf, email, phone)
    VALUES ('PF', 'Maria da Silva', '123.456.789-00', 'maria.silva@test.com', '(11) 91234-5678')
    RETURNING donor_id
), 

donor_pj AS (
    INSERT INTO donor (donor_type, company_name, cnpj, email, phone)
    VALUES ('PJ', 'Doacoes Unidas LTDA', '12.345.678/0001-90', 'contato@doacoesunidas.com', '(11) 3344-5566')
    RETURNING donor_id
), 

product_arroz AS (
    INSERT INTO product (name, category, unit)
    VALUES ('Arroz', 'Alimento', 'kg')
    RETURNING product_id
), 

product_leite AS (
    INSERT INTO product (name, category, unit)
    VALUES ('Leite em Pó', 'Alimento', 'kg')
    RETURNING product_id
), 

product_cesta AS (
    INSERT INTO product (name, category, unit)
    VALUES ('Cesta Básica', 'Kit', 'unidade')
    RETURNING product_id
), 

beneficiary_ana AS (
    INSERT INTO beneficiary (name, cpf, birth_date, address, city, household_size, family_income)
    VALUES ('Ana Pereira', '987.654.321-00', '1985-06-15', 'Rua das Flores, 123', 'São Paulo', 4, 850.00)
    RETURNING beneficiary_id
), 

beneficiary_joao AS (
    INSERT INTO beneficiary (name, cpf, birth_date, address, city, household_size, family_income)
    VALUES ('João Souza', '111.222.333-44', '1990-11-20', 'Avenida Central, 456', 'Campinas', 3, 1200.00)
    RETURNING beneficiary_id
), 

donation_food AS (
    INSERT INTO donation (donor_id, donation_date, donation_type, total_value)
    SELECT donor_id, '2026-04-10', 'food', 200.00 FROM donor_pf
    RETURNING donation_id
), 

donation_financial AS (
    INSERT INTO donation (donor_id, donation_date, donation_type, total_value)
    SELECT donor_id, '2026-04-12', 'financial', 500.00 FROM donor_pj
    RETURNING donation_id
), 

donation_item1 AS (
    INSERT INTO donation_item (donation_id, product_id, quantity)
    SELECT donation_id, product_id, 50.00 FROM donation_food, product_arroz
    RETURNING donation_item_id
), 

donation_item2 AS (
    INSERT INTO donation_item (donation_id, product_id, quantity)
    SELECT donation_id, product_id, 30.00 FROM donation_food, product_leite
    RETURNING donation_item_id
), 

donation_item3 AS (
    INSERT INTO donation_item (donation_id, product_id, quantity)
    SELECT donation_id, product_id, 10.00 FROM donation_financial, product_cesta
    RETURNING donation_item_id
), 

inventory_arroz AS (
    INSERT INTO inventory (product_id, quantity, batch, expiration_date)
    SELECT product_id, 50.00, 'BATCH-ARZ-001', '2026-12-31' FROM product_arroz
    RETURNING inventory_id
), 

inventory_leite AS (
    INSERT INTO inventory (product_id, quantity, batch, expiration_date)
    SELECT product_id, 30.00, 'BATCH-LEI-001', '2026-10-31' FROM product_leite
    RETURNING inventory_id
), 

inventory_cesta AS (
    INSERT INTO inventory (product_id, quantity, batch, expiration_date)
    SELECT product_id, 10.00, 'BATCH-CES-001', '2026-08-31' FROM product_cesta
    RETURNING inventory_id
), 

distribution_ana AS (
    INSERT INTO distribution (beneficiary_id, distribution_date)
    SELECT beneficiary_id, '2026-04-15' FROM beneficiary_ana
    RETURNING distribution_id
), 

distribution_joao AS (
    INSERT INTO distribution (beneficiary_id, distribution_date)
    SELECT beneficiary_id, '2026-04-18' FROM beneficiary_joao
    RETURNING distribution_id
), 

distribution_item1 AS (
    INSERT INTO distribution_item (distribution_id, product_id, quantity)
    SELECT distribution_id, product_id, 5.00 FROM distribution_ana, product_arroz
    RETURNING distribution_item_id
), 

distribution_item2 AS (
    INSERT INTO distribution_item (distribution_id, product_id, quantity)
    SELECT distribution_id, product_id, 2.00 FROM distribution_ana, product_leite
    RETURNING distribution_item_id
), 

distribution_item3 AS (
    INSERT INTO distribution_item (distribution_id, product_id, quantity)
    SELECT distribution_id, product_id, 1.00 FROM distribution_joao, product_cesta
    RETURNING distribution_item_id
), 

inventory_movement_entry_arroz AS (
    INSERT INTO inventory_movement (product_id, movement_type, quantity, movement_date, source)
    SELECT product_id, 'entry', 50.00, CURRENT_TIMESTAMP, 'donation' FROM product_arroz
    RETURNING inventory_movement_id
), 

inventory_movement_entry_leite AS (
    INSERT INTO inventory_movement (product_id, movement_type, quantity, movement_date, source)
    SELECT product_id, 'entry', 30.00, CURRENT_TIMESTAMP, 'donation' FROM product_leite
    RETURNING inventory_movement_id
), 

inventory_movement_exit_ana AS (
    INSERT INTO inventory_movement (product_id, movement_type, quantity, movement_date, source)
    SELECT product_id, 'exit', 7.00, CURRENT_TIMESTAMP, 'distribution' FROM product_arroz
    RETURNING inventory_movement_id
)
SELECT 1;

-- Usuários do sistema
INSERT INTO system_user (name, email, password_hash, role)
VALUES
    ('Administrador', 'admin@test.com', '$2b$12$EXAMPLEHASHEDPASSWORD1234567890abcdefghijklmn', 'admin'),
    ('Operador', 'operator@test.com', '$2b$12$EXAMPLEHASHEDPASSWORD1234567890abcdefghijklmn', 'operator');

COMMIT;
