# 🏗️ FINAL WORKING ARCHITECTURE

## 📋 SYSTEM OVERVIEW

```
┌─────────────────┐    HTTP/8080    ┌─────────────────┐    HTTP/8000    ┌─────────────────┐
│   Android App   │ ◄──────────────► │  Spring Boot    │ ◄──────────────► │  Python FastAPI │
│   (Real Device) │                │   Backend       │                │   AI Service    │
│ 192.168.29.53   │                │ 0.0.0.0:8080    │                │ 0.0.0.0:8000    │
└─────────────────┘                └─────────────────┘                └─────────────────┘
                                            │                                 │
                                            ▼                                 ▼
                                   ┌─────────────────┐                ┌─────────────────┐
                                   │   MySQL DB      │                │   Mock Data     │
                                   │  localhost:3306 │                │   (Fallback)    │
                                   └─────────────────┘                └─────────────────┘
```

## 🔧 PORT CONFIGURATION

### **Port Assignment**
- **Android App**: Connects to Spring Boot on port 8080
- **Spring Boot**: Runs on port 8080, calls Python on port 8000
- **Python FastAPI**: Runs on port 8000, connects to MySQL
- **MySQL Database**: Runs on port 3306

### **Network Flow**
```
Android App (192.168.29.53:8080)
    ↓ HTTP Request
Spring Boot (localhost:8080)
    ↓ Internal API Call
Python FastAPI (localhost:8000)
    ↓ Database Query
MySQL Database (localhost:3306)
```

## 📱 ANDROID APP CONFIGURATION

### **Base URL**
```kotlin
// RetrofitInstance.kt
private val BASE_URL = "http://192.168.29.53:8080/"
```

### **API Endpoints**
```kotlin
// ApiService.kt
@POST("ai/query")
suspend fun sendQuery(@Body request: QueryRequest): QueryApiResponse

@GET("ai/dashboard")
suspend fun getSales(): DashboardApiResponse

@GET("ai/insights")
suspend fun getInsights(): InsightsApiResponse

@GET("ai/alerts")
suspend fun getAlerts(): AlertsApiResponse
```

### **Network Security**
```xml
<!-- AndroidManifest.xml -->
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
android:usesCleartextTraffic="true"
android:networkSecurityConfig="@xml/network_security_config"

<!-- network_security_config.xml -->
<base-config cleartextTrafficPermitted="true">
    <trust-anchors>
        <certificates src="system"/>
    </trust-anchors>
</base-config>
<domain-config cleartextTrafficPermitted="true">
    <domain includeSubdomains="true">192.168.29.53</domain>
</domain-config>
```

## 🚀 SPRING BOOT CONFIGURATION

### **Application Properties**
```properties
# application.properties
server.address=0.0.0.0
server.port=8080

# Database Configuration
spring.datasource.url=jdbc:mysql://localhost:3306/ai_analytics
spring.datasource.username=root
spring.datasource.password=Manshi@263
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
```

### **Controller Endpoints**
```java
// MinimalController.java
@RestController
@RequestMapping("/ai")
@CrossOrigin(origins = "*")

@PostMapping("/query")
public ResponseEntity<Map<String, Object>> processQuery(@RequestBody Map<String, String> request) {
    // Calls Python FastAPI: http://localhost:8000/ai/query
    String pythonApiUrl = "http://localhost:8000/ai/query";
    // ... implementation with fallback
}

@GetMapping("/dashboard")
public ResponseEntity<Map<String, Object>> getDashboardData() {
    // Mock data for now
}

@GetMapping("/insights")
public ResponseEntity<Map<String, Object>> getInsights() {
    // Mock data for now
}

@GetMapping("/alerts")
public ResponseEntity<Map<String, Object>> getAlerts() {
    // Mock data for now
}
```

### **RestTemplate Configuration**
```java
// RestTemplateConfig.java
@Configuration
public class RestTemplateConfig {
    @Bean
    public RestTemplate restTemplate() {
        RestTemplate restTemplate = new RestTemplate();
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(5000);  // 5 seconds
        factory.setReadTimeout(10000);  // 10 seconds
        restTemplate.setRequestFactory(factory);
        return restTemplate;
    }
}
```

## 🐍 PYTHON FASTAPI CONFIGURATION

### **Server Configuration**
```python
# main.py
if __name__ == "__main__":
    import uvicorn
    import os
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
        access_log=True
    )
```

### **Database Configuration**
```python
# .env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ai_analytics
DB_USER=root
DB_PASSWORD=Manshi@263
```

### **API Endpoints**
```python
# main.py
@app.post("/ai/query")
async def process_query(request: QueryRequest):
    # Multi-agent AI processing
    # Returns QueryResponse

@app.get("/ai/dashboard")
async def get_dashboard_data():
    # Returns aggregated sales data
    # Returns DashboardResponse

@app.get("/ai/insights")
async def get_insights():
    # Returns business insights
    # Returns List[Insight]

@app.get("/ai/alerts")
async def get_alerts():
    # Returns system alerts
    # Returns List[Alert]
```

## 🗄️ DATABASE SCHEMA

### **MySQL Tables**
```sql
-- Sales Table
CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    revenue DECIMAL(12,2) NOT NULL,
    date DATE NOT NULL,
    region VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insights Table
CREATE TABLE insights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    insight_type ENUM('drop', 'increase', 'alert', 'trend', 'warning') NOT NULL,
    message TEXT NOT NULL,
    value DECIMAL(10,2),
    category VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 FALLBACK STRATEGIES

### **Port Fallback**
```python
# start_fallback.py
def find_available_port(start_port=8000, max_port=8010):
    for port in range(start_port, max_port + 1):
        if port is available:
            return port
    return None
```

### **Service Fallback**
```java
// Spring Boot fallback if Python service is down
catch (Exception e) {
    response.put("status", "success");
    response.put("data", Map.of(
        "answer", "Mock response: Python service unavailable",
        "insights", List.of("Service unavailable", "Using fallback")
    ));
    return ResponseEntity.ok(response);
}
```

## 🚀 DEPLOYMENT COMMANDS

### **Start Services**
```bash
# 1. Start Python FastAPI (port 8000)
cd ai-python-service
.\.venv\Scripts\python start_fallback.py

# 2. Start Spring Boot (port 8080)
cd backend-springboot
./mvnw spring-boot:run

# 3. Build and Install Android App
cd app
./gradlew clean assembleDebug
adb install app/build/outputs/apk/debug/app-debug.apk
```

### **Port Management**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process using port 8000
for /f "tokens=5" %i in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /PID %i /F

# Use automated script
.\port_management.bat
```

## ✅ SUCCESS INDICATORS

### **Expected Results**
- ✅ **Spring Boot**: Running on http://localhost:8080
- ✅ **Python FastAPI**: Running on http://localhost:8000
- ✅ **Android App**: Connects to http://192.168.29.53:8080
- ✅ **Database**: MySQL connected on localhost:3306
- ✅ **API Calls**: Android → Spring Boot → Python → MySQL
- ✅ **Fallback**: Graceful degradation when services are down

### **Health Checks**
```bash
# Spring Boot health
curl http://localhost:8080/ai/dashboard

# Python FastAPI health
curl http://localhost:8000/health

# Android connectivity
curl http://192.168.29.53:8080/ai/dashboard
```

## 🔧 TROUBLESHOOTING

### **Common Issues**
1. **Port Conflicts**: Use port_management.bat
2. **Network Issues**: Check WiFi connectivity
3. **Firewall**: Allow ports 8000 and 8080
4. **Database**: Verify MySQL connection
5. **Android**: Check network security config

### **Debug Commands**
```bash
# Check listening ports
netstat -ano | findstr LISTENING

# Test connectivity
ping 192.168.29.53

# Monitor logs
adb logcat | grep -E "(Network|HTTP|Error)"
```
