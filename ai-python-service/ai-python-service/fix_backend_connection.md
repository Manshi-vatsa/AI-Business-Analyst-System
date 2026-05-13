# 🔧 BACKEND CONNECTION FIX GUIDE

## 🚨 ISSUE IDENTIFIED
- Android app cannot connect to backend
- Spring Boot backend not starting properly due to Java path issues
- Python FastAPI is running but Spring Boot is not accessible

## 🎯 SOLUTION STEPS

### **Step 1: Fix Java Environment**
```powershell
# Set correct Java path
$env:JAVA_HOME = "C:\Program Files\Java\jdk-17.0.12"
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"

# Verify Java
java -version
```

### **Step 2: Start Spring Boot Backend**
```powershell
cd "D:\AI_Business_Analyst_System\backend-springboot"

# Method 1: Using Maven Wrapper
.\mvnw spring-boot:run

# Method 2: If Maven fails, build and run JAR
.\mvnw clean package -DskipTests
java -jar target\*.jar
```

### **Step 3: Start Python FastAPI**
```powershell
cd "D:\AI_Business_Analyst_System\ai-python-service"
.\.venv\Scripts\python main.py
```

### **Step 4: Test Backend Connectivity**
```powershell
# Test Spring Boot
curl http://localhost:8080/ai/health

# Test Python FastAPI
curl http://localhost:8000/health

# Test from Android device
curl http://192.168.29.53:8080/ai/health
```

## 🛠️ ANDROID APP FIXES

### **1. Update Base URL Configuration**
```kotlin
// RetrofitInstance.kt
private const val BASE_URL = "http://192.168.29.53:8080/"
```

### **2. Add Connection Testing**
```kotlin
// ChatActivity.kt - Add this method
private fun testBackendConnection() {
    lifecycleScope.launch {
        try {
            val response = apiRepository.healthCheck()
            if (response.isSuccess) {
                Toast.makeText(this, "✅ Backend connected", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "❌ Backend unreachable", Toast.LENGTH_LONG).show()
            }
        } catch (e: Exception) {
            Toast.makeText(this, "❌ Connection failed: ${e.message}", Toast.LENGTH_LONG).show()
        }
    }
}
```

### **3. Add Fallback for Offline Mode**
```kotlin
// ApiRepository.kt - Add fallback
suspend fun sendQuery(question: String): Result<QueryResponse> {
    return try {
        val result = apiRepository.sendQuery(question)
        result
    } catch (e: Exception) {
        // Return mock data when backend is unavailable
        Result.success(getMockQueryResponse(question))
    }
}

private fun getMockQueryResponse(question: String): QueryResponse {
    return QueryResponse(
        status = "success",
        data = QueryData(
            answer = "Mock response for: $question (Backend unavailable)",
            insights = listOf("Backend is not running", "Please start backend services")
        ),
        message = "Using mock data",
        timestamp = java.time.Instant.now().toString()
    )
}
```

## 📱 ANDROID MANIFEST CONFIGURATION

### **1. Network Permissions**
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
```

### **2. Cleartext Traffic**
```xml
<application
    android:usesCleartextTraffic="true"
    android:networkSecurityConfig="@xml/network_security_config">
```

### **3. Network Security Config**
```xml
<!-- res/xml/network_security_config.xml -->
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="false">192.168.29.53</domain>
        <domain includeSubdomains="false">localhost</domain>
    </domain-config>
</network-security-config>
```

## 🔍 DEBUGGING STEPS

### **1. Check Backend Services**
```powershell
# Check if ports are listening
netstat -an | findstr ":8080"
netstat -an | findstr ":8000"

# Check Spring Boot logs
Get-Content backend-springboot\logs\ai-analytics.log -Tail 10
```

### **2. Test Network Connectivity**
```powershell
# Test from laptop
Test-NetConnection -ComputerName 192.168.29.53 -Port 8080

# Test from Android device (using adb)
adb shell ping 192.168.29.53
```

### **3. Monitor Android Logs**
```powershell
# Monitor Android app logs
adb logcat | grep -E "(ChatActivity|Network|HTTP|Error)"
```

## 🚀 QUICK START COMMANDS

### **Start All Services**
```powershell
# Terminal 1 - Start Spring Boot
cd "D:\AI_Business_Analyst_System\backend-springboot"
$env:JAVA_HOME = "C:\Program Files\Java\jdk-17.0.12"
.\mvnw spring-boot:run

# Terminal 2 - Start Python FastAPI
cd "D:\AI_Business_Analyst_System\ai-python-service"
.\.venv\Scripts\python main.py

# Terminal 3 - Build and Install Android App
cd "D:\AI_Business_Analyst_System\app"
.\gradlew assembleDebug
adb install app\build\outputs\apk\debug\app-debug.apk
```

## 📊 EXPECTED RESULTS

### **Backend Services Status**
- ✅ Spring Boot running on http://192.168.29.53:8080
- ✅ Python FastAPI running on http://192.168.29.53:8000
- ✅ Both services responding to health checks

### **Android App Behavior**
- ✅ App connects to backend on startup
- ✅ Shows "✅ Connected to backend" message
- ✅ Chat functionality works with real backend
- ✅ Fallback to mock data if backend unavailable

### **Network Configuration**
- ✅ Device and laptop on same WiFi network
- ✅ IP address 192.168.29.53 accessible from device
- ✅ HTTP traffic allowed for development

## 🎯 FINAL VERIFICATION

### **Test Complete Flow**
1. Start both backend services
2. Install and open Android app
3. Check connection status in app
4. Send a test query in chat
5. Verify response from backend
6. Test with backend stopped (should show fallback)

**🎉 Your complete system should now work end-to-end!**
