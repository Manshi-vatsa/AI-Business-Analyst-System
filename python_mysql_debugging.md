# 🔧 PYTHON FASTAPI MYSQL DEBUGGING GUIDE

## 🚨 COMMON ERRORS & SOLUTIONS

### **1. Unknown Column 'sale_date'**
```
Error: Unknown column 'sale_date' in 'field list'
```

**✅ SOLUTION:**
- Fixed all references from `sale_date` to `date` in:
  - `data_agent.py` - SQL queries
  - `analysis_agent.py` - DataFrame operations
  - `database_schema.sql` - Schema definition

**🔍 VERIFICATION:**
```bash
mysql -u root -pManshi@263 -e "DESCRIBE ai_analytics.sales;"
# Should show 'date' column, not 'sale_date'
```

### **2. SQL Syntax Error Near '%s'**
```
Error: SQL syntax error near '%s'
```

**✅ SOLUTION:**
- Added proper parameterized queries
- Created `execute_insert_query()` method
- Fixed `cursor.execute(sql, params)` usage

**🔍 VERIFICATION:**
```python
# Test parameterized query
data_agent = DataAgent()
data_agent.execute_insert_query(
    "INSERT INTO insights (type, message, value, category) VALUES (%s, %s, %s, %s)",
    ("test", "test message", 10.5, "test")
)
```

### **3. Missing Commit After Insert**
```
Error: Data not appearing in database
```

**✅ SOLUTION:**
- Added `connection.commit()` in `execute_insert_query()`
- Added rollback on error
- Proper connection management

**🔍 VERIFICATION:**
```bash
mysql -u root -pManshi@263 -e "SELECT * FROM ai_analytics.insights ORDER BY created_at DESC LIMIT 5;"
```

## 📋 DEBUGGING STEPS

### **Step 1: Database Schema Validation**
```bash
# Check sales table structure
mysql -u root -pManshi@263 -e "DESCRIBE ai_analytics.sales;"

# Check insights table structure  
mysql -u root -pManshi@263 -e "DESCRIBE ai_analytics.insights;"

# Verify sample data exists
mysql -u root -pManshi@263 -e "SELECT COUNT(*) as sales_count FROM ai_analytics.sales;"
```

### **Step 2: Python Connection Test**
```bash
cd ai-python-service
.\.venv\Scripts\python -c "
from database_connection import DatabaseConnection
db = DatabaseConnection()
print('Connection test:', db.test_connection())
print('Connection info:', db.get_connection_info())
"
```

### **Step 3: Query Execution Test**
```bash
.\.venv\Scripts\python -c "
from agents.data_agent import DataAgent
agent = DataAgent()
try:
    results = agent.execute_query('SELECT * FROM sales LIMIT 5')
    print('Query successful:', len(results), 'records')
    if results:
        print('Sample record:', results[0])
except Exception as e:
    print('Query failed:', e)
"
```

### **Step 4: Insert Operation Test**
```bash
.\.venv\Scripts\python -c "
from agents.data_agent import DataAgent
agent = DataAgent()
try:
    affected = agent.execute_insert_query(
        'INSERT INTO insights (type, message, value, category) VALUES (%s, %s, %s, %s)',
        ('debug', 'Debug test insertion', 99.9, 'test')
    )
    print('Insert successful:', affected, 'rows affected')
except Exception as e:
    print('Insert failed:', e)
"
```

### **Step 5: API Endpoint Test**
```bash
# Start FastAPI server
.\.venv\Scripts\python main.py

# Test endpoints in another terminal
curl http://localhost:8000/health
curl http://localhost:8000/ai/dashboard
curl -X POST http://localhost:8000/ai/query -H "Content-Type: application/json" -d '{"question":"test"}'
```

## 🔧 SPECIFIC DEBUG SCENARIOS

### **Scenario 1: Column Name Mismatch**
```bash
# Check what columns exist
mysql -u root -pManshi@263 -e "SHOW COLUMNS FROM ai_analytics.sales;"

# Check Python code expectations
.\.venv\Scripts\python -c "
import pandas as pd
from agents.data_agent import DataAgent
agent = DataAgent()
data = agent.get_data('get all sales', ['get sales data'])
if data:
    df = pd.DataFrame(data)
    print('Available columns:', list(df.columns))
else:
    print('No data retrieved')
"
```

### **Scenario 2: Parameter Binding Issues**
```bash
# Test parameter binding manually
mysql -u root -pManshi@263 -e "
PREPARE test_stmt FROM 'INSERT INTO insights (type, message, value, category) VALUES (?, ?, ?, ?)';
SET @type = 'test', @message = 'test', @value = 10.5, @category = 'test';
EXECUTE test_stmt USING @type, @message, @value, @category;
DEALLOCATE PREPARE test_stmt;
"
```

### **Scenario 3: Connection Issues**
```bash
# Test MySQL connection from Python
.\.venv\Scripts\python -c "
import mysql.connector
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Manshi@263',
        database='ai_analytics'
    )
    print('Connection successful')
    cursor = conn.cursor()
    cursor.execute('SELECT 1')
    print('Query successful:', cursor.fetchone())
    conn.close()
except Exception as e:
    print('Connection failed:', e)
"
```

## 📊 EXPECTED RESULTS

### **Successful Query Execution**
```python
# Expected output for query test
Query successful: 15 records
Sample record: {'id': 1, 'product': 'Laptop', 'quantity': 25, 'revenue': 125000.0, 'date': '2024-01-15', 'region': 'North'}
```

### **Successful Insert Operation**
```python
# Expected output for insert test
Insert successful: 1 rows affected
```

### **Successful API Response**
```json
// Expected API response
{
  "status": "success",
  "data": {
    "monthlySales": [{"month": "2024-01", "revenue": 75000.0}],
    "regionSales": [{"region": "North", "revenue": 125000.0}],
    "productSales": [{"product": "Laptop", "revenue": 125000.0}]
  },
  "message": "Dashboard data retrieved successfully"
}
```

## 🚀 PERFORMANCE OPTIMIZATION

### **Database Indexes**
```sql
-- Verify indexes exist
SHOW INDEX FROM ai_analytics.sales;
SHOW INDEX FROM ai_analytics.insights;

-- Add missing indexes if needed
CREATE INDEX idx_sales_date ON ai_analytics.sales(date);
CREATE INDEX idx_sales_product ON ai_analytics.sales(product);
CREATE INDEX idx_insights_type ON ai_analytics.insights(type);
```

### **Connection Pooling**
```python
# In database_connection.py, add connection pooling
self.db_config.update({
    'pool_size': 5,
    'pool_reset_session': True,
    'autocommit': True,
    'get_warnings': True
})
```

## 📱 FRONTEND INTEGRATION

### **Android App Testing**
```bash
# Test from Android device
curl http://192.168.29.53:8000/ai/dashboard

# Expected JSON structure
{
  "status": "success",
  "data": {
    "monthlySales": [...],
    "regionSales": [...],
    "productSales": [...]
  },
  "message": "Dashboard data retrieved successfully",
  "timestamp": "2024-01-23T15:45:00Z"
}
```

### **Spring Boot Integration**
```bash
# Test Spring Boot calling Python API
curl -X POST http://localhost:8080/ai/query -H "Content-Type: application/json" -d '{"question":"What are total sales?"}'
```

## 🔍 LOG ANALYSIS

### **Enable Debug Logging**
```python
# In main.py, set debug level
import logging
logging.basicConfig(level=logging.DEBUG)

# Check logs for SQL queries
tail -f logs/ai-analytics.log | grep "SQL Query"
```

### **Common Log Patterns**
```
✅ SUCCESS: "Executing SQL query: SELECT * FROM sales ORDER BY date DESC LIMIT 100"
✅ SUCCESS: "Query executed successfully, returned 15 records"
✅ SUCCESS: "INSERT query executed successfully, affected 1 rows"

❌ ERROR: "Error executing query: Unknown column 'sale_date'"
❌ ERROR: "Error executing INSERT query: SQL syntax error near '%s'"
```

## 🎯 FINAL VERIFICATION CHECKLIST

- [ ] **Database Schema**: All columns match Python code expectations
- [ ] **Column Names**: No more `sale_date` references, all use `date`
- [ ] **Parameterized Queries**: All INSERT operations use proper parameter binding
- [ ] **Commit Operations**: All INSERT operations include `connection.commit()`
- [ ] **API Responses**: JSON structure matches frontend expectations
- [ ] **Error Handling**: Proper exceptions and fallback mechanisms
- [ ] **Logging**: Comprehensive logging for debugging
- [ ] **Performance**: Appropriate indexes and connection management

**🎉 Your Python FastAPI backend should now work correctly with MySQL!**
