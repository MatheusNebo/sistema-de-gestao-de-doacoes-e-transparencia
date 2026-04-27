-- =====================
-- DONOR
-- =====================
CREATE TABLE donor (
    donor_id SERIAL,

    donor_type CHAR(2) NOT NULL,

    name VARCHAR(150),
    cpf VARCHAR(14),

    company_name VARCHAR(150),
    cnpj VARCHAR(18),

    email VARCHAR(150),
    phone VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_donor PRIMARY KEY (donor_id),

    CONSTRAINT chk_donor_type CHECK (donor_type IN ('PF','PJ')),

    CONSTRAINT uq_donor_cpf UNIQUE (cpf),
    CONSTRAINT uq_donor_cnpj UNIQUE (cnpj),

    CONSTRAINT chk_donor_pf_pj CHECK (
        (donor_type = 'PF' AND name IS NOT NULL AND cpf IS NOT NULL AND cnpj IS NULL AND company_name IS NULL)
        OR
        (donor_type = 'PJ' AND company_name IS NOT NULL AND cnpj IS NOT NULL AND cpf IS NULL AND name IS NULL)
    )
);

-- =====================
-- PRODUCT
-- =====================
CREATE TABLE product (
    product_id SERIAL,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    unit VARCHAR(20) NOT NULL,

    CONSTRAINT pk_product PRIMARY KEY (product_id)
);

-- =====================
-- DONATION
-- =====================
CREATE TABLE donation (
    donation_id SERIAL,

    donor_id INT NOT NULL,
    donation_date DATE NOT NULL,
    donation_type VARCHAR(20) NOT NULL,
    total_value NUMERIC(10,2),

    CONSTRAINT pk_donation PRIMARY KEY (donation_id),

    CONSTRAINT fk_donation_donor
        FOREIGN KEY (donor_id)
        REFERENCES donor(donor_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_donation_type
        CHECK (donation_type IN ('food','financial'))
);

-- =====================
-- DONATION ITEM
-- =====================
CREATE TABLE donation_item (
    donation_item_id SERIAL,

    donation_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity NUMERIC(10,2) NOT NULL,

    CONSTRAINT pk_donation_item PRIMARY KEY (donation_item_id),

    CONSTRAINT fk_donation_item_donation
        FOREIGN KEY (donation_id)
        REFERENCES donation(donation_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_donation_item_product
        FOREIGN KEY (product_id)
        REFERENCES product(product_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_donation_item_quantity
        CHECK (quantity > 0)
);

-- =====================
-- INVENTORY
-- =====================
CREATE TABLE inventory (
    inventory_id SERIAL,

    product_id INT NOT NULL,
    quantity NUMERIC(10,2) NOT NULL,
    batch VARCHAR(50),
    expiration_date DATE NOT NULL,
    entry_date DATE DEFAULT CURRENT_DATE,

    CONSTRAINT pk_inventory PRIMARY KEY (inventory_id),

    CONSTRAINT fk_inventory_product
        FOREIGN KEY (product_id)
        REFERENCES product(product_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_inventory_quantity
        CHECK (quantity >= 0)
);

-- =====================
-- BENEFICIARY
-- =====================
CREATE TABLE beneficiary (
    beneficiary_id SERIAL,

    name VARCHAR(150) NOT NULL,
    cpf VARCHAR(14) NOT NULL,
    birth_date DATE,
    address TEXT,
    city VARCHAR(100),

    household_size INT,
    family_income NUMERIC(10,2),

    created_at DATE DEFAULT CURRENT_DATE,

    CONSTRAINT pk_beneficiary PRIMARY KEY (beneficiary_id),

    CONSTRAINT uq_beneficiary_cpf UNIQUE (cpf),

    CONSTRAINT chk_household_size
        CHECK (household_size > 0),

    CONSTRAINT chk_family_income
        CHECK (family_income >= 0)
);

-- =====================
-- DISTRIBUTION
-- =====================
CREATE TABLE distribution (
    distribution_id SERIAL,

    beneficiary_id INT NOT NULL,
    distribution_date DATE NOT NULL,

    CONSTRAINT pk_distribution PRIMARY KEY (distribution_id),

    CONSTRAINT fk_distribution_beneficiary
        FOREIGN KEY (beneficiary_id)
        REFERENCES beneficiary(beneficiary_id)
        ON DELETE RESTRICT
);

-- =====================
-- DISTRIBUTION ITEM
-- =====================
CREATE TABLE distribution_item (
    distribution_item_id SERIAL,

    distribution_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity NUMERIC(10,2) NOT NULL,

    CONSTRAINT pk_distribution_item PRIMARY KEY (distribution_item_id),

    CONSTRAINT fk_distribution_item_distribution
        FOREIGN KEY (distribution_id)
        REFERENCES distribution(distribution_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_distribution_item_product
        FOREIGN KEY (product_id)
        REFERENCES product(product_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_distribution_quantity
        CHECK (quantity > 0)
);

-- =====================
-- SYSTEM USER
-- =====================
CREATE TABLE system_user (
    user_id SERIAL,

    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20),

    CONSTRAINT pk_user PRIMARY KEY (user_id),

    CONSTRAINT uq_user_email UNIQUE (email),

    CONSTRAINT chk_user_role
        CHECK (role IN ('admin','operator'))
);

-- =====================
-- INVENTORY MOVEMENT
-- =====================
CREATE TABLE inventory_movement (
    inventory_movement_id SERIAL,

    product_id INT NOT NULL,
    movement_type VARCHAR(20) NOT NULL,
    quantity NUMERIC(10,2) NOT NULL,
    movement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(50),

    CONSTRAINT pk_inventory_movement PRIMARY KEY (inventory_movement_id),

    CONSTRAINT fk_inventory_movement_product
        FOREIGN KEY (product_id)
        REFERENCES product(product_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_movement_type
        CHECK (movement_type IN ('entry','exit','loss')),

    CONSTRAINT chk_movement_quantity
        CHECK (quantity > 0),

    CONSTRAINT chk_movement_source
        CHECK (source IN ('donation','distribution','adjustment'))
);