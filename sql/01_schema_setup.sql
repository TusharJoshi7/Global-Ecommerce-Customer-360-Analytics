-- =====================================================================
-- E-Commerce Analytics Database Schema DDL & Staging Tables
-- Author: Tushar Joshi | Data Analyst Portfolio
-- Database Engine: PostgreSQL / MySQL / SQLite compatible SQL script
-- =====================================================================

DROP TABLE IF EXISTS raw_transactions;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;

-- 1. Customers Table DDL
CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    region VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Products Table DDL
CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL
);

-- 3. Orders Table DDL
CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    order_date TIMESTAMP NOT NULL,
    customer_id VARCHAR(50) REFERENCES customers(customer_id),
    product_id VARCHAR(50) REFERENCES products(product_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL,
    gross_amount NUMERIC(12, 2) NOT NULL,
    discount_pct NUMERIC(5, 2) DEFAULT 0.00,
    discount_amount NUMERIC(10, 2) DEFAULT 0.00,
    net_amount NUMERIC(12, 2) NOT NULL,
    shipping_cost NUMERIC(10, 2) DEFAULT 0.00,
    total_revenue NUMERIC(12, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    order_status VARCHAR(50) NOT NULL
);

-- Index creation for performance optimization on large analytical datasets
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX idx_orders_status ON orders(order_status);
CREATE INDEX idx_orders_category ON orders(product_id);
