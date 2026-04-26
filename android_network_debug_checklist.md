# 🔧 ANDROID NETWORK CONNECTIVITY DEBUG CHECKLIST

## 📋 PRE-FLIGHT CHECKLIST

### ✅ Server Configuration
- [ ] Spring Boot running on port 8000 (not 8080)
- [ ] Server binding to 0.0.0.0 (not localhost only)
- [ ] Windows firewall allows port 8000
- [ ] Laptop and phone on same WiFi network
- [ ] IP address: 192.168.29.53

### ✅ Android Configuration
- [ ] INTERNET permission in AndroidManifest.xml
- [ ] usesCleartextTraffic="true" in AndroidManifest.xml
- [ ] Network security config allows 192.168.29.53
- [ ] Base URL: http://192.168.29.53:8000/
- [ ] API endpoints: /ai/query, /ai/dashboard, /ai/insights, /ai/alerts

## 🚀 STEP-BY-STEP DEBUG

### Step 1: Verify Spring Boot Server
```bash
# Start Spring Boot
cd backend-springboot
./mvnw spring-boot:run

# Test locally
curl http://localhost:8000/ai/dashboard

# Test from phone (run this on laptop)
curl http://192.168.29.53:8000/ai/dashboard
```

### Step 2: Fix Windows Firewall
```bash
# Run as administrator
.\firewall_fix.bat

# Or manually:
netsh advfirewall firewall add rule name="Allow Port 8000" dir=in action=allow protocol=TCP localport=8000
```

### Step 3: Test Network Connectivity
```bash
# From laptop
ping 192.168.29.53

# From phone (use browser)
http://192.168.29.53:8000/ai/dashboard
```

### Step 4: Verify Android App
```bash
# Rebuild APK
cd app
./gradlew assembleDebug

# Install on phone
adb install app/build/outputs/apk/debug/app-debug.apk
```

## 🔍 DEBUG COMMANDS

### Test All Endpoints
```bash
# Dashboard
curl http://192.168.29.53:8000/ai/dashboard

# Query
curl -X POST http://192.168.29.53:8000/ai/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What are total sales?"}'

# Insights
curl http://192.168.29.53:8000/ai/insights

# Alerts
curl http://192.168.29.53:8000/ai/alerts
```

### Check Server Status
```bash
# Check if port 8000 is listening
netstat -an | findstr :8000

# Check firewall rules
netsh advfirewall firewall show rule name="Allow Port 8000"
```

## 🐛 COMMON ISSUES & SOLUTIONS

### Issue: "failed to connect to /192.168.29.53:8000"
**Solutions:**
1. Check Spring Boot is running on port 8000
2. Verify server.address=0.0.0.0 in application.properties
3. Add Windows firewall rule for port 8000
4. Ensure phone and laptop on same WiFi

### Issue: 404 Not Found
**Solutions:**
1. Verify endpoint mapping: /ai/* not /api/*
2. Check MinimalController has @RequestMapping("/ai")
3. Ensure all endpoints exist: query, dashboard, insights, alerts

### Issue: Network Security Exception
**Solutions:**
1. Set usesCleartextTraffic="true" in AndroidManifest.xml
2. Add 192.168.29.53 to network_security_config.xml
3. Set base-config cleartextTrafficPermitted="true"

### Issue: Connection Timeout
**Solutions:**
1. Check WiFi connectivity
2. Verify IP address is correct
3. Test with browser first
4. Check firewall blocking

## 📱 ANDROID TESTING

### Install and Test
```bash
# Build APK
cd app
./gradlew clean assembleDebug

# Install via ADB
adb install app/build/outputs/apk/debug/app-debug.apk

# Monitor logs
adb logcat | grep -E "(Network|HTTP|Error|Exception)"
```

### Test Network from Phone
1. Open browser on phone
2. Navigate to: http://192.168.29.53:8000/ai/dashboard
3. Should see JSON response

## 🔧 FINAL VERIFICATION

### Expected Results
- ✅ Spring Boot responds on http://192.168.29.53:8000
- ✅ All endpoints return 200 OK
- ✅ Android app connects without errors
- ✅ Dashboard shows data
- ✅ Chat functionality works

### Success Indicators
```
Spring Boot logs: "Started AiAnalyticsApplication on port 8000"
Android logs: "HTTP 200 - OK"
Dashboard: Shows charts and data
Chat: Responses from backend
```
