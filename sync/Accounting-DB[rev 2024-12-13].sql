-- Table mst_users
CREATE TABLE mst_users (
 id BIGSERIAL PRIMARY KEY,
 name VARCHAR(255),
 email VARCHAR(255),
 password VARCHAR(255)
);

-- Table mst_roles
CREATE TABLE mst_roles (
 id BIGSERIAL PRIMARY KEY,
 name VARCHAR(255),
 description TEXT
);

-- Table mst_permissions
CREATE TABLE mst_permissions (
 id BIGSERIAL PRIMARY KEY,
 name VARCHAR(255),
 description TEXT
);

-- Table mst_actions
CREATE TABLE mst_actions (
 id BIGSERIAL PRIMARY KEY,
 name VARCHAR(255),
 description TEXT
);

-- Tabel mst_menus
CREATE TABLE mst_menus (
 id BIGSERIAL PRIMARY KEY,
 parent_id BIGINT REFERENCES mst_menus(id),
 name VARCHAR(255),
 route VARCHAR(255),
 icon VARCHAR(255),
 order INT
);

-- Table ref_role_menus
CREATE TABLE ref_role_menus (
 role_id BIGINT REFERENCES mst_roles(id),
 menu_id BIGINT REFERENCES mst_menus(id),
 PRIMARY KEY (role_id, menu_id)
);

-- Table ref_user_menus
CREATE TABLE ref_user_menus (
 user_id BIGINT REFERENCES mst_users(id),
 menu_id BIGINT REFERENCES mst_menus(id),
 PRIMARY KEY (user_id, menu_id)
);

-- Table ref_user_roles
CREATE TABLE ref_user_roles (
 user_id BIGINT REFERENCES mst_users(id),
 role_id BIGINT REFERENCES mst_roles(id),
 PRIMARY KEY (user_id, role_id)
);

-- Table ref_user_permissions
CREATE TABLE ref_user_permissions (
 user_id BIGINT REFERENCES mst_users(id),
 permission_id BIGINT REFERENCES mst_permissions(id),
 PRIMARY KEY (user_id, permission_id)
);

-- Table ref_role_permissions
CREATE TABLE ref_role_permissions (
 role_id BIGINT REFERENCES mst_roles(id),
 permission_id BIGINT REFERENCES mst_permissions(id),
 PRIMARY KEY (role_id, permission_id)
);

-- Table audit_logs
CREATE TABLE audit_logs (
 id BIGSERIAL PRIMARY KEY,
 user_id BIGINT REFERENCES mst_users(id),
 action_id BIGINT REFERENCES mst_actions(id),
 record_id VARCHAR(20) NOT NULL,
 ip_address VARCHAR(20) NOT NULL,
 model_name VARCHAR(100) NOT NULL,
 notes TEXT DEFAULT NULL,
 actioned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table mst_companies
CREATE TABLE mst_companies (
 id VARCHAR(10) PRIMARY KEY,
 name VARCHAR(255),
 address TEXT,
 contact_email VARCHAR(255)
);

-- Table ref_user_companies
CREATE type RefUserCompanyStatus AS ENUM ('pending', 'approved', 'rejected');
CREATE TABLE ref_user_companies (
 user_id BIGINT REFERENCES mst_users(id),
 company_id VARCHAR(10) REFERENCES mst_companies(id),
 status RefUserCompanyStatus DEFAULT 'pending',
 PRIMARY KEY (user_id, company_id)
);

-- Table mst_account_types
CREATE TABLE mst_account_types (
 id BIGSERIAL PRIMARY KEY,
 name VARCHAR(255)
);

-- Table mst_account_categories
CREATE TABLE mst_account_categories (
 id BIGSERIAL PRIMARY KEY,
 name VARCHAR(255)
);

-- Table mst_account_tags
CREATE TABLE mst_account_tags (
 id BIGSERIAL PRIMARY KEY,
 name VARCHAR(255)
);

-- Table mst_account_levels
CREATE TABLE mst_account_levels (
 id BIGSERIAL PRIMARY KEY,
 name VARCHAR(50),
 level INT
);

-- Table mst_analytic_accounts
CREATE TABLE mst_analytic_accounts (
 id BIGSERIAL PRIMARY KEY,
 name VARCHAR(50)
);

-- Table mst_taxes
CREATE TABLE mst_taxes (
 id BIGSERIAL PRIMARY KEY,
 name VARCHAR(50),
 scope VARCHAR(50),
 tax FLOAT DEFAULT 0
);

-- Table mst_currencies
CREATE TABLE mst_currencies (
 code VARCHAR(10) PRIMARY KEY,
 name VARCHAR(50),
 country VARCHAR(50)
);

-- Table mst_accounts
CREATE TABLE mst_accounts (
 code VARCHAR(20) PRIMARY KEY,
 parent_code VARCHAR(20) REFERENCES mst_accounts(code),
 account_level_id BIGINT REFERENCES mst_account_levels(id),
 account_type_id BIGINT REFERENCES mst_account_types(id),
 account_category_id BIGINT REFERENCES mst_account_categories(id),
 analytic_account_id BIGINT REFERENCES mst_analytic_accounts(id),
 tax_id BIGINT REFERENCES mst_taxes(id),
 tag_id BIGINT REFERENCES mst_account_tags(id),
 currency_code VARCHAR(10) REFERENCES mst_currencies(code) DEFAULT 'IDR',
 name VARCHAR(255),
 initial_balance DECIMAL(15, 2),
 current_balance DECIMAL(15, 2),
 reconciliation BOOLEAN DEFAULT NULL,
 deprecated BOOLEAN DEFAULT NULL
);

-- Table mst_journal_types
CREATE TABLE mst_journal_types (
 id BIGSERIAL PRIMARY KEY,
 name VARCHAR(255)
);

-- Table mst_journals
CREATE TABLE mst_journals (
 id BIGSERIAL PRIMARY KEY,
 journal_type_id BIGINT REFERENCES mst_journal_types(id),
 name VARCHAR(255)
);

-- Table trs_journal_entries
CREATE TYPE TrsJournalEntryStatus AS ENUM ('posted', 'unposted');
CREATE TABLE trs_journal_entries (
 id VARCHAR(20) PRIMARY KEY,
 journal_id BIGINT REFERENCES mst_journals(id),
 entry_date DATE,
 description TEXT,
 status TrsJournalEntryStatus DEFAULT 'unposted'
);

-- Table trs_journal_entry_details
CREATE TABLE trs_journal_entry_details (
 id BIGSERIAL PRIMARY KEY,
 journal_entry_id VARCHAR(20) REFERENCES trs_journal_entries(id),
 account_code VARCHAR(20) REFERENCES mst_accounts(code),
 debit DECIMAL(15, 2),
 credit DECIMAL(15, 2)
);

-- Table trs_balance_sheets
CREATE TABLE trs_balance_sheets (
 id VARCHAR(20) PRIMARY KEY,
 period_start DATE,
 period_end DATE,
 total_assets DECIMAL(15, 2),
 total_liabilities DECIMAL(15, 2),
 equity DECIMAL(15, 2)
);

-- Table trs_profit_and_loss
CREATE TABLE trs_profit_and_loss (
 id VARCHAR(20) PRIMARY KEY,
 period_start DATE,
 period_end DATE,
 total_revenue DECIMAL(15, 2),
 total_expenses DECIMAL(15, 2),
 net_profit DECIMAL(15, 2)
);

-- Table trs_operational_transactions
CREATE TABLE trs_operational_transactions (
 id BIGSERIAL PRIMARY KEY,
 operational_data JSONB,
 processed BOOLEAN DEFAULT FALSE
);

-- -- FOR INERT DATA
-- -- Insert data untuk mst_users
--INSERT INTO mst_users (name, email, password)
--VALUES 
--('John Doe', 'john.doe@mail.com', 'JDJiJDEyJGx4M3hVNGxkeWdaZUtNV3FVamdDdi56MXZoeTljVjBmNTkzQ01OQVNaN1pTLjN6OG4xVy4y'),
--('Jane Smith', 'jane.smith@mail.com', 'JDJiJDEyJGx4M3hVNGxkeWdaZUtNV3FVamdDdi56MXZoeTljVjBmNTkzQ01OQVNaN1pTLjN6OG4xVy4y');
--
-- -- Insert data untuk mst_roles
--INSERT INTO mst_roles (name, description)
--VALUES 
--('Admin', 'Administrator with full access'),
--('User', 'Regular user with limited access');
--
-- -- Insert data untuk mst_permissions
--INSERT INTO mst_permissions (name, description)
--VALUES 
--('create_user', 'Create new user'),
--('edit_user', 'Edit existing user'),
--('delete_user', 'Delete user');
--
-- -- Insert data untuk mst_actions
--INSERT INTO mst_actions (name, description)
--VALUES 
--('create', 'Create a new record'),
--('update', 'Update an existing record'),
--('delete', 'Delete a record');
--
-- -- Insert data untuk ref_user_roles
--INSERT INTO ref_user_roles (user_id, role_id)
--VALUES 
--(1, 1), -- John Doe sebagai Admin
--(2, 2); -- Jane Smith sebagai User
--
-- -- Insert data untuk ref_user_permissions
--INSERT INTO ref_user_permissions (user_id, permission_id)
--VALUES 
--(1, 1), -- John Doe punya permission create_user
--(1, 2), -- John Doe punya permission edit_user
--(2, 1); -- Jane Smith punya permission create_user
--
-- -- Insert data untuk ref_role_permissions
--INSERT INTO ref_role_permissions (role_id, permission_id)
--VALUES 
--(1, 1), -- Admin role punya permission create_user
--(1, 2), -- Admin role punya permission edit_user
--(2, 3); -- User role punya permission delete_user
--
-- -- Insert data untuk mst_companies
--INSERT INTO mst_companies (id, name, address, contact_email)
--VALUES 
--('COMP001', 'Company One', '123 Company St, City A', 'contact@companyone.com'),
--('COMP002', 'Company Two', '456 Company Ave, City B', 'contact@companytwo.com');
--
-- -- Insert data untuk ref_user_companies
--INSERT INTO ref_user_companies (user_id, company_id, status)
--VALUES 
--(1, 'COMP001', 'approved'),
--(2, 'COMP002', 'pending');
--
-- -- Insert data untuk mst_account_types
--INSERT INTO mst_account_types (name)
--VALUES 
--('Asset'),
--('Liability'),
--('Equity');
--
-- -- Insert data untuk mst_account_categories
--INSERT INTO mst_account_categories (name)
--VALUES 
--('Current Assets'),
--('Current Liabilities'),
--('Fixed Assets');
--
-- -- Insert data untuk mst_account_tags
--INSERT INTO mst_account_tags (name)
--VALUES 
--('Tag1'),
--('Tag2');
--
-- -- Insert data untuk mst_account_levels
--INSERT INTO mst_account_levels (name, level)
--VALUES 
--('Level 1', 1),
--('Level 2', 2);
--
-- -- Insert data untuk mst_analytic_accounts
--INSERT INTO mst_analytic_accounts (name)
--VALUES 
--('Analytic Account 1'),
--('Analytic Account 2');
--
-- -- Insert data untuk mst_taxes
--INSERT INTO mst_taxes (name, scope, tax)
--VALUES 
--('VAT', 'Domestic', 10.0),
--('Sales Tax', 'International', 5.0);
--
-- -- Insert data untuk mst_currencies
--INSERT INTO mst_currencies (code, name, country)
--VALUES 
--('IDR', 'Indonesian Rupiah', 'Indonesia'),
--('USD', 'US Dollar', 'United States');
--
-- -- Insert data untuk mst_accounts
--INSERT INTO mst_accounts (code, parent_code, account_level_id, account_type_id, account_category_id, analytic_account_id, tax_id, tag_id, currency_code, name, initial_balance, current_balance)
--VALUES 
--('101', NULL, 1, 1, 1, 1, 1, 1, 'IDR', 'Cash', 1000000.00, 1000000.00),
--('202', NULL, 1, 2, 2, 2, 2, 2, 'USD', 'Accounts Payable', 500000.00, 500000.00);
--
-- -- Insert data untuk mst_journal_types
--INSERT INTO mst_journal_types (name)
--VALUES 
--('General Journal'),
--('Sales Journal');
--
-- -- Insert data untuk mst_journals
--INSERT INTO mst_journals (journal_type_id, name)
--VALUES 
--(1, 'General Ledger Journal'),
--(2, 'Sales Journal');
--
-- -- Insert data untuk trs_journal_entries
--INSERT INTO trs_journal_entries (id, journal_id, entry_date, description, status)
--VALUES 
--('JE001', 1, '2024-12-01', 'General journal entry for company one', 'unposted'),
--('JE002', 2, '2024-12-01', 'Sales journal entry for company two', 'posted');
--
-- -- Insert data untuk trs_journal_entry_details
--INSERT INTO trs_journal_entry_details (journal_entry_id, account_code, debit, credit)
--VALUES 
--('JE001', '101', 1000000.00, 0.00), -- Cash Debit
--('JE001', '202', 0.00, 500000.00), -- Accounts Payable Credit
--('JE002', '101', 500000.00, 0.00), -- Cash Debit
--('JE002', '202', 0.00, 500000.00); -- Accounts Payable Credit
--
-- -- Insert data untuk trs_balance_sheets
--INSERT INTO trs_balance_sheets (id, period_start, period_end, total_assets, total_liabilities, equity)
--VALUES 
--('BS001', '2024-12-01', '2024-12-31', 1500000.00, 500000.00, 1000000.00);
--
-- -- Insert data untuk trs_profit_and_loss
--INSERT INTO trs_profit_and_loss (id, period_start, period_end, total_revenue, total_expenses, net_profit)
--VALUES 
--('PL001', '2024-12-01', '2024-12-31', 2000000.00, 1000000.00, 1000000.00);
--
-- -- Insert data untuk trs_operational_transactions
--INSERT INTO trs_operational_transactions (operational_data, processed)
--VALUES 
--('{"transaction_id": "TX001", "amount": 1000000, "currency": "IDR"}', FALSE),
--('{"transaction_id": "TX002", "amount": 500000, "currency": "USD"}', TRUE);
--
-- -- Insert data untuk audit_logs
--INSERT INTO audit_logs (user_id, action_id, record_id, ip_address, model_name, notes, actioned_at)
--VALUES 
--(1, 1, 'JE001', '192.168.1.1', 'trs_journal_entries', 'Created a journal entry', '2024-12-01 10:00:00'),
--(2, 2, 'JE002', '192.168.1.2', 'trs_journal_entries', 'Updated a journal entry', '2024-12-02 11:00:00');

-- -- ALTER TABLE mst_accounts RENAME COLUMN account_level_id TO account_account_level_id;


-- -- select (name, level) from mst_account_levels mal 


