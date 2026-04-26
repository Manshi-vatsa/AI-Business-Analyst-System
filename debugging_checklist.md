# 🔧 DEBUGGING CHECKLIST

## 📋 PRE-FLIGHT CHECKS

### ✅ Environment Setup
- [ ] **Java 17+** installed and configured
- [ ] **Python 3.12+** with virtual environment
- [ ] **MySQL 8+** running and accessible
- [ ] **Android Studio** with API level 33+
- [ ] **Physical Android device** connected via USB
- [ ] **Same WiFi network** for laptop and phone

### ✅ Port Configuration
- [ ] **Spring Boot**: Port 8080 (application.properties)
- [ ] **Python FastAPI**: Port 8000 (start_fallback.py)
- [ ] **MySQL**: Port 3306 (default)
- [ ] **No port conflicts**: Check with `netstat -ano | findstr :8000`

### ✅ Network Configuration
- [ ] **Windows Firewall**: Allow ports 8000 and 8080
- [ ] **Android Manifest**: INTERNET permission + cleartext traffic
- [ ] **Network Security Config**: 192.168.29.53 allowed
- [ ] **IP Address**: 192.168.29.53 (laptop WiFi)

## 🚀 STEP-BY-STEP DEBUG

### **Step 1: Database Connection**
```bash
# Test MySQL connection
mysql -u root -pManshi@263 -e "SHOW DATABASES;"

# Create database if needed
mysql -u root -pManshi@263 < ai-python-service/database_schema.sql

# Verify tables
mysql -u root -pManshi@263 -e "USE ai_analytics; SHOW TABLES;"
```

### **Step 2: Python FastAPI Service**
```bash
# Start Python service with fallback
cd ai-python-service
.\.venv\Scripts\python start_fallback.py

# Test Python service
curl http://localhost:8000/health
curl http://localhost:8000/ai/dashboard

# Check logs for errors
# Look for "Port 8000 is blocked" or "Using port 8001"
```

### **Step 3: Spring Boot Backend**
```bash
# Start Spring Boot
cd backend-springboot
./mvnw spring-boot:run

# Test Spring Boot endpoints
curl http://localhost:8080/ai/dashboard
curl -X POST http://localhost:8080/ai/query -d '{"question":"test"}'

# Check Spring Boot logs for Python service connection
```

### **Step 4: Android App Connection**
```bash
# Build and install APK
cd app
./gradlew clean assembleDebug
adb install app/build/outputs/apk/debug/app-debug.apk

# Monitor Android logs
adb logcat | grep -E "(Network|HTTP|Error|Exception)"

# Test from phone browser
http://192.168.29.53:8080/ai/dashboard
```

## 🔍 SPECIFIC DEBUG SCENARIOS

### **Scenario 1: Port Already in Use**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process
.\port_management.bat

# Or manual kill
for /f "tokens=5" %i in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /PID %i /F
```

### **Scenario 2: Python Service Not Starting**
```bash
# Check virtual environment
.\.venv\Scripts\python --version

# Check dependencies
.\.venv\Scripts\pip list | findstr fastapi

# Test Python import
.\.venv\Scripts\python -c "from main import app; print('FastAPI import successful')"

# Use fallback script
.\.venv\Scripts\python start_fallback.py
```

### **Scenario 3: Spring Boot Can't Connect to Python**
```bash
# Test Python service from Spring Boot perspective
curl http://localhost:8000/ai/query -X POST -H "Content-Type: application/json" -d '{"question":"test"}'

# Check Spring Boot logs for connection errors
# Look for "Python service unavailable" or "Connection refused"

# Test with different port if Python is on 8001
# Update MinimalController.java pythonApiUrl
```

### **Scenario 4: Android App Can't Connect**
```bash
# Test from laptop (should work)
curl http://192.168.29.53:8080/ai/dashboard

# Test from phone browser
http://192.168.29.53:8080/ai/dashboard

# Check Android network permissions
adb shell dumpsys package com.example.aianalytics | grep permission

# Monitor network requests
adb logcat | grep -E "(OkHttp|Retrofit|Network)"
```

### **Scenario 5: Database Connection Issues**
```bash
# Test MySQL connection from Python
.\.venv\Scripts\python -c "
from database_connection import DatabaseConnection
db = DatabaseConnection()
print('Connection test:', db.test_connection())
"

# Test MySQL connection from Spring Boot
# Check Spring Boot logs for database errors
# Look for "Access denied" or "Connection refused"

# Verify MySQL user and password
mysql -u root -pManshi@263 -e "SELECT USER(), DATABASE();"
```

## 🐛 COMMON ERROR MESSAGES

### **"Port 8000 already in use"**
```bash
# Solution: Kill process or use fallback script
.\port_management.bat
# or
.\.venv\Scripts\python start_fallback.py
```

### **"Permission denied"**
```bash
# Solution: Run as administrator
# Right-click Command Prompt → "Run as administrator"
```

### **"Failed to connect to /192.168.29.53:8080"**
```bash
# Solution: Check network configuration
# 1. Verify IP address: ipconfig
# 2. Check WiFi connectivity
# 3. Test from phone browser
# 4. Check firewall rules
```

### **"Connection refused"**
```bash
# Solution: Check if service is running
# 1. Verify Spring Boot is running on port 8080
# 2. Verify Python is running on port 8000
# 3. Check binding to 0.0.0.0 (not localhost)
```

### **"Access denied for user 'root'@'localhost'"**
```bash
# Solution: Fix MySQL authentication
mysql -u root -p -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Manshi@263';"
```

## 📊 SUCCESS VERIFICATION

### **Expected Results**
```bash
# Python FastAPI
curl http://localhost:8000/health
# Expected: {"status": "healthy", "timestamp": "...", "service": "AI Business Analyst Service"}

# Spring Boot
curl http://localhost:8080/ai/dashboard
# Expected: {"status": "success", "data": {...}, "message": "Dashboard data retrieved successfully"}

# Android App
# Expected: Dashboard shows charts, Chat responds with AI answers
```

### **Health Check Commands**
```bash
# All services should respond with 200 OK
curl -w "%{http_code}\n" http://localhost:8000/health -o /dev/null
curl -w "%{http_code}\n" http://localhost:8080/ai/dashboard -o /dev/null
curl -w "%{http_code}\n" http://192.168.29.53:8080/ai/dashboard -o /dev/null
```

## 🔧 ADVANCED DEBUGGING

### **Enable Detailed Logging**
```bash
# Spring Boot debug mode
./mvnw spring-boot:run -Dspring-boot.run.arguments="--debug"

# Python FastAPI debug mode
.\.venv\Scripts\python -c "
import uvicorn
from main import app
uvicorn.run(app, host='0.0.0.0', port=8000, log_level='debug')
"

# Android debug logging
adb logcat -s "AIAnalytics:*"
```

### **Network Monitoring**
```bash
# Monitor network connections
netstat -an | findstr :8000
netstat -an | findstr :8080

# Monitor Android network traffic
adb shell dumpsys netstats

# Test with different tools
# Use Postman/Insomnia for API testing
# Use Wireshark for deep packet inspection
```

### **Database Monitoring**
```bash
# Monitor MySQL connections
mysql -u root -pManshi@263 -e "SHOW PROCESSLIST;"

# Monitor database performance
mysql -u root -pManshi@263 -e "SHOW STATUS LIKE 'Connections';"
```

## 📱 ANDROID SPECIFIC DEBUG

### **ADB Commands**
```bash
# Check device connectivity
adb devices

# Install APK
adb install app/build/outputs/apk/debug/app-debug.apk

# Monitor logs
adb logcat | grep -E "(AIAnalytics|Network|HTTP)"

# Clear app data
adb shell pm clear com.example.aianalytics

# Force stop app
adb shell am force-stop com.example.aianalytics
```

### **Network Debug**
```bash
# Test network from device
adb shell ping 192.168.29.53

# Check network configuration
adb shell dumpsys connectivity

# Test HTTP from device
adb shell curl http://192.168.29.53:8080/ai/dashboard
```

## 🎯 FINAL VERIFICATION CHECKLIST

### **Before Starting**
- [ ] MySQL running and accessible
- [ ] Virtual environment activated
- [ ] No port conflicts
- [ ] Firewall configured
- [ ] Android device connected

### **After Starting Services**
- [ ] Python FastAPI responds on port 8000
- [ ] Spring Boot responds on port 8080
- [ ] Spring Boot can call Python API
- [ ] Database connections work
- [ ] Android app can connect to Spring Boot

### **Functional Testing**
- [ ] Dashboard shows data
- [ ] Chat functionality works
- [ ] Error handling works (fallback)
- [ ] Network errors are handled gracefully
- [ ] App works on real device

**🎉 System is ready when all checks pass!**
