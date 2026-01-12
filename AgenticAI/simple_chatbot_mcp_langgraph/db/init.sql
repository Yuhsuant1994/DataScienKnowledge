-- Initialize sales database schema
-- This script runs automatically when Postgres container starts

-- Create sales_order table
CREATE TABLE IF NOT EXISTS sales_order (
    order_id VARCHAR(20) PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    city VARCHAR(100)
);

-- Create order_details table
CREATE TABLE IF NOT EXISTS order_details (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL,
    amount DECIMAL(10, 2),
    profit DECIMAL(10, 2),
    quantity INTEGER,
    category VARCHAR(50),
    sub_category VARCHAR(50),
    FOREIGN KEY (order_id) REFERENCES sales_order(order_id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_order_details_order_id ON order_details(order_id);
CREATE INDEX IF NOT EXISTS idx_order_details_category ON order_details(category);
CREATE INDEX IF NOT EXISTS idx_sales_order_date ON sales_order(order_date);
CREATE INDEX IF NOT EXISTS idx_sales_order_state ON sales_order(state);

-- Set date format to match CSV (DD-MM-YYYY)
SET datestyle = 'DMY';

-- Create temporary tables to load data (allows filtering nulls)
CREATE TEMP TABLE temp_sales_order (
    order_id VARCHAR(20),
    order_date TEXT,
    customer_name VARCHAR(100),
    state VARCHAR(100),
    city VARCHAR(100)
);

CREATE TEMP TABLE temp_order_details (
    order_id VARCHAR(20),
    amount TEXT,
    profit TEXT,
    quantity TEXT,
    category VARCHAR(50),
    sub_category VARCHAR(50)
);

-- Load data from CSV files into temp tables
COPY temp_sales_order(order_id, order_date, customer_name, state, city)
FROM '/data/sales_order.csv'
DELIMITER ','
CSV HEADER;

COPY temp_order_details(order_id, amount, profit, quantity, category, sub_category)
FROM '/data/order_details.csv'
DELIMITER ','
CSV HEADER;

-- Insert only non-null rows into actual tables
INSERT INTO sales_order (order_id, order_date, customer_name, state, city)
SELECT order_id, order_date::DATE, customer_name, state, city
FROM temp_sales_order
WHERE order_id IS NOT NULL AND order_id != '';

INSERT INTO order_details (order_id, amount, profit, quantity, category, sub_category)
SELECT order_id, amount::DECIMAL, profit::DECIMAL, quantity::INTEGER, category, sub_category
FROM temp_order_details
WHERE order_id IS NOT NULL AND order_id != '';

-- Create a view for common queries (optional but useful)
CREATE OR REPLACE VIEW sales_summary AS
SELECT
    so.order_id,
    so.order_date,
    so.customer_name,
    so.state,
    so.city,
    od.category,
    od.sub_category,
    od.quantity,
    od.amount,
    od.profit
FROM sales_order so
JOIN order_details od ON so.order_id = od.order_id;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE sales_db TO chatbot_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO chatbot_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO chatbot_user;
