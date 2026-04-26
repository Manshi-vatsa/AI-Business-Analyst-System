-- ==========================================
-- MySQL 8+ Authentication Fix Commands
-- ==========================================

-- STEP 1: Check current authentication plugin
SELECT plugin, host, user FROM mysql.user WHERE user='root';

-- STEP 2: Change authentication plugin to mysql_native_password (for local development)
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Manshi@263';

-- STEP 3: Flush privileges to apply changes
FLUSH PRIVILEGES;

-- STEP 4: Verify the change
SELECT plugin, host, user FROM mysql.user WHERE user='root';

-- STEP 5: Test connection (you can run this after Spring Boot starts)
-- SHOW PROCESSLIST;

-- ==========================================
-- Alternative: Create dedicated application user
-- ==========================================

-- Create new user with mysql_native_password
CREATE USER 'ai_analytics_app'@'localhost' IDENTIFIED WITH mysql_native_password BY 'StrongAppPassword123!';

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON ai_analytics.* TO 'ai_analytics_app'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;

-- ==========================================
-- Production: Keep caching_sha2_password with SSL
-- ==========================================

-- For production, keep caching_sha2_password but ensure SSL is enabled
-- ALTER USER 'root'@'localhost' REQUIRE SSL;
-- ALTER USER 'ai_analytics_app'@'localhost' REQUIRE SSL;
