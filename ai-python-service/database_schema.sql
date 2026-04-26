-- ==========================================
-- AI ANALYTICS DATABASE SCHEMA
-- ==========================================

-- Create database
CREATE DATABASE IF NOT EXISTS ai_analytics 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE ai_analytics;

-- ==========================================
-- SALES TABLE
-- ==========================================
CREATE TABLE IF NOT EXISTS sales (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    product VARCHAR(100) DEFAULT NULL,
    region VARCHAR(100) DEFAULT NULL,
    revenue DECIMAL(19,2) NOT NULL,
    date DATE DEFAULT NULL,
    quantity INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_date (date),
    INDEX idx_region (region),
    INDEX idx_product (product),
    INDEX idx_revenue (revenue)
);

-- ==========================================
-- INSIGHTS TABLE
-- ==========================================
CREATE TABLE IF NOT EXISTS insights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(50) DEFAULT NULL,
    message TEXT DEFAULT NULL,
    value DOUBLE DEFAULT NULL,
    category VARCHAR(100) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_type (type),
    INDEX idx_category (category),
    INDEX idx_created_at (created_at)
);

-- ==========================================
-- SAMPLE DATA (IF NEEDED)
-- ==========================================
INSERT IGNORE INTO sales (product, quantity, revenue, date, region) VALUES
('Laptop', 25, 125000.00, '2024-01-15', 'North'),
('Phone', 35, 70000.00, '2024-01-16', 'South'),
('Tablet', 20, 60000.00, '2024-01-17', 'East'),
('Laptop', 18, 90000.00, '2024-01-18', 'West'),
('Phone', 40, 80000.00, '2024-01-19', 'North'),
('Tablet', 15, 45000.00, '2024-01-20', 'South'),
('Laptop', 30, 150000.00, '2024-01-21', 'East'),
('Phone', 22, 44000.00, '2024-01-22', 'West'),
('Tablet', 18, 54000.00, '2024-01-23', 'North'),
('Laptop', 16, 80000.00, '2024-01-24', 'South'),
('Phone', 20, 40000.00, '2024-01-25', 'East'),
('Tablet', 10, 30000.00, '2024-01-26', 'West'),
('Laptop', 12, 60000.00, '2024-01-27', 'North'),
('Phone', 15, 30000.00, '2024-01-28', 'South'),
('Tablet', 8, 24000.00, '2024-01-29', 'East');

INSERT IGNORE INTO insights (insight_type, message, value, category) VALUES
('drop', 'Sales decreased by 15% this week', -15.00, 'sales'),
('increase', 'North region showed 20% growth', 20.00, 'region'),
('alert', 'Phone inventory running low', 5.00, 'inventory'),
('trend', 'Laptop sales trending upward', 25.00, 'product'),
('warning', 'South region below target', -10.00, 'region');
