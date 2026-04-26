# 🔧 API DEBUGGING STEP-BY-STEP GUIDE

## 📋 DEBUGGING WORKFLOW

### **Step 1: Test Python FastAPI Directly**
```bash
# Start Python FastAPI
cd ai-python-service
.\.venv\Scripts\python main.py

# Test endpoints directly
curl http://localhost:8000/health
curl http://localhost:8000/ai/dashboard
curl -X POST http://localhost:8000/ai/query -H "Content-Type: application/json" -d '{"question":"What are total sales?"}'
```

**Expected Python Response:**
```json
{
  "status": "success",
  "data": {
    "monthlySales": [{"month": "2024-01", "revenue": 75000.0}],
    "regionSales": [{"region": "North", "revenue": 125000.0}],
    "productSales": [{"product": "Laptop", "revenue": 125000.0}]
  },
  "message": "Dashboard data retrieved successfully",
  "timestamp": "2024-01-23T15:45:00Z"
}
```

### **Step 2: Test Spring Boot Backend**
```bash
# Start Spring Boot
cd backend-springboot
./mvnw spring-boot:run

# Test Spring Boot endpoints
curl http://localhost:8080/ai/dashboard
curl -X POST http://localhost:8080/ai/query -H "Content-Type: application/json" -d '{"question":"What are total sales?"}'
```

**Expected Spring Boot Response:**
```json
{
  "status": "success",
  "data": {
    "monthlySales": [{"month": "2024-01", "revenue": 75000.0}],
    "regionSales": [{"region": "North", "revenue": 125000.0}],
    "productSales": [{"product": "Laptop", "revenue": 125000.0}]
  },
  "message": "Dashboard data retrieved successfully",
  "timestamp": "2024-01-23T15:45:00Z"
}
```

### **Step 3: Test Android App Connection**
```bash
# Install and test Android app
cd app
./gradlew clean assembleDebug
adb install app/build/outputs/apk/debug/app-debug.apk

# Monitor Android logs
adb logcat | grep -E "(AIAnalytics_Network|Network|HTTP|Error|Exception)"
```

**Expected Android Logs:**
```
=== API REQUEST ===
Endpoint: /ai/dashboard
Method: GET
==================
=== API RESPONSE ===
Endpoint: /ai/dashboard
Status: 200 OK
Success: true
Body: {"status":"success","data":{"monthlySales":[...]}}
Validating dashboard JSON structure...
✓ Found field: status
✓ Found field: data
✓ Found field: message
✓ Found monthlySales with 2 items
===================
```

## 🔍 SPECIFIC DEBUG SCENARIOS

### **Scenario 1: Dashboard Not Loading**
```bash
# 1. Check Python FastAPI
curl -v http://localhost:8000/ai/dashboard

# 2. Check Spring Boot logs
tail -f backend-springboot/logs/ai-analytics.log | grep "DASHBOARD"

# 3. Check Android logs
adb logcat | grep "dashboard"

# 4. Validate JSON structure
curl http://localhost:8000/ai/dashboard | python -m json.tool
```

### **Scenario 2: API Sometimes Returns Error**
```bash
# 1. Check service health
curl http://localhost:8000/health
curl http://localhost:8080/ai/health

# 2. Test with different payloads
curl -X POST http://localhost:8080/ai/query -H "Content-Type: application/json" -d '{"question":"test"}'
curl -X POST http://localhost:8080/ai/query -H "Content-Type: application/json" -d '{"question":""}'
curl -X POST http://localhost:8080/ai/query -H "Content-Type: application/json" -d '{}'

# 3. Check database connection
mysql -u root -pManshi@263 -e "SELECT COUNT(*) FROM ai_analytics.sales;"
```

### **Scenario 3: JSON Structure Mismatch**
```bash
# 1. Compare Python vs Spring Boot responses
echo "=== PYTHON RESPONSE ==="
curl http://localhost:8000/ai/dashboard | python -m json.tool

echo "=== SPRING BOOT RESPONSE ==="
curl http://localhost:8080/ai/dashboard | python -m json.tool

# 2. Validate field names
curl http://localhost:8000/ai/dashboard | jq 'keys'
curl http://localhost:8080/ai/dashboard | jq 'keys'
```

## 🚀 ISOLATION CHECKLIST

### **Check 1: Database Layer**
```bash
# Verify database is running
mysql -u root -pManshi@263 -e "SHOW DATABASES;"

# Verify tables exist
mysql -u root -pManshi@263 -e "USE ai_analytics; SHOW TABLES;"

# Verify data exists
mysql -u root -pManshi@263 -e "SELECT COUNT(*) FROM ai_analytics.sales;"
mysql -u root -pManshi@263 -e "SELECT COUNT(*) FROM ai_analytics.insights;"

# Verify column names
mysql -u root -pManshi@263 -e "DESCRIBE ai_analytics.sales;"
mysql -u root -pManshi@263 -e "DESCRIBE ai_analytics.insights;"
```

### **Check 2: Python FastAPI Layer**
```bash
# Test database connection from Python
.\.venv\Scripts\python -c "
from database_connection import DatabaseConnection
db = DatabaseConnection()
print('Connection test:', db.test_connection())
"

# Test query execution
.\.venv\Scripts\python -c "
from agents.data_agent import DataAgent
agent = DataAgent()
results = agent.execute_query('SELECT * FROM sales LIMIT 5')
print('Query results:', len(results))
"

# Test API endpoints
curl -w "%{http_code}\n" http://localhost:8000/health -o /dev/null
curl -w "%{http_code}\n" http://localhost:8000/ai/dashboard -o /dev/null
```

### **Check 3: Spring Boot Layer**
```bash
# Test Spring Boot health
curl -w "%{http_code}\n" http://localhost:8080/actuator/health -o /dev/null

# Test Spring Boot endpoints
curl -w "%{http_code}\n" http://localhost:8080/ai/dashboard -o /dev/null

# Check Spring Boot logs
tail -f backend-springboot/logs/ai-analytics.log | grep -E "(ERROR|WARN)"
```

### **Check 4: Android Layer**
```bash
# Test network connectivity
adb shell ping 192.168.29.53

# Test HTTP from device
adb shell curl http://192.168.29.53:8080/ai/dashboard

# Monitor Android logs
adb logcat -s "AIAnalytics_Network"
```

## 📊 EXPECTED RESULTS MATRIX

| Layer | Status | Expected Response | Debug Command |
|-------|--------|------------------|---------------|
| Database | ✅ | Connected, tables exist | `mysql -u root -pManshi@263 -e "SHOW TABLES;"` |
| Python FastAPI | ✅ | 200 OK, valid JSON | `curl http://localhost:8000/ai/dashboard` |
| Spring Boot | ✅ | 200 OK, valid JSON | `curl http://localhost:8080/ai/dashboard` |
| Android | ✅ | Dashboard loads | `adb logcat | grep "AIAnalytics_Network"` |

## 🔧 COMMON FIXES

### **Fix 1: Database Column Mismatch**
```sql
-- Fix column names if needed
ALTER TABLE insights CHANGE insight_type type VARCHAR(50);
ALTER TABLE insights CHANGE insight_type type VARCHAR(50) DEFAULT NULL;
```

### **Fix 2: JSON Field Name Mismatch**
```python
# Fix Python JSON structure
dashboard_data = {
    "monthlySales": monthly_sales,  # ✅ Correct
    "regionSales": region_sales,    # ✅ Correct
    "productSales": product_sales   # ✅ Correct
}
```

### **Fix 3: Spring Boot DTO Mismatch**
```java
// Fix Java DTO field names
@JsonProperty("monthlySales")
private List<Map<String, Object>> monthlySales;  // ✅ Correct
```

### **Fix 4: Network Connectivity**
```bash
# Check firewall
netsh advfirewall firewall show rule name="Allow Port 8000"
netsh advfirewall firewall show rule name="Allow Port 8080"

# Check IP address
ipconfig
ping 192.168.29.53
```

## 📱 ANDROID SPECIFIC DEBUG

### **Enable Debug Logging**
```kotlin
// In your API calls
NetworkLogger.logRequest("/ai/dashboard", "GET")
val startTime = System.currentTimeMillis()

// In response handling
val endTime = System.currentTimeMillis()
NetworkLogger.logResponse("/ai/dashboard", response)
NetworkLogger.logTiming("/ai/dashboard", startTime, endTime)
```

### **Monitor Network Traffic**
```bash
# Monitor all network requests
adb logcat | grep -E "(OkHttp|Retrofit|Network)"

# Monitor specific errors
adb logcat | grep -E "(ERROR|Exception|Failed)"
```

## 🎯 FINAL VERIFICATION

### **Complete System Test**
```bash
# 1. Start all services
cd ai-python-service && .\.venv\Scripts\python main.py &
cd backend-springboot && ./mvnw spring-boot:run &

# 2. Test complete flow
curl -X POST http://localhost:8080/ai/query -H "Content-Type: application/json" -d '{"question":"What are total sales?"}'

# 3. Test Android app
adb install app/build/outputs/apk/debug/app-debug.apk
adb logcat | grep "AIAnalytics_Network"
```

### **Success Indicators**
- ✅ **Database**: Connected, tables exist, data available
- ✅ **Python FastAPI**: Responds with valid JSON
- ✅ **Spring Boot**: Proxies requests correctly
- ✅ **Android**: Receives and parses JSON successfully
- ✅ **Dashboard**: Loads and displays data
- ✅ **Chat**: Processes queries and returns responses

**🎉 Your complete system should now work end-to-end!**
