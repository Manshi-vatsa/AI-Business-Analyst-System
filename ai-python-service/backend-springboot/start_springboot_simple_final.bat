@echo off
echo ========================================
echo SIMPLE SPRING BOOT STARTUP
echo ========================================

echo.
echo 1. Setting up Java environment...
set JAVA_HOME=C:\Program Files\Java\jdk-17
set PATH=%JAVA_HOME%\bin;%PATH%

echo Java version:
java -version

echo.
echo 2. Changing to backend directory...
cd /d "D:\AI_Business_Analyst_System\backend-springboot"

echo.
echo 3. Building project first...
echo Building with Maven...
call .\mvnw clean compile

echo.
echo 4. Starting Spring Boot...
echo Starting Spring Boot...
call .\mvnw spring-boot:run

echo.
echo 5. Testing connection...
timeout /t 20 /nobreak > nul

echo Testing health endpoint...
curl -s http://localhost:8080/ai/health && (
    echo ✅ SUCCESS: Spring Boot is running!
    echo URL: http://localhost:8080
    echo Health: http://localhost:8080/ai/health
    echo Android should connect to: http://192.168.29.53:8080
) || (
    echo ⚠️ Spring Boot may still be starting...
    echo Please wait 30 seconds for full startup
)

echo.
echo ========================================
echo STARTUP COMPLETE
echo ========================================
pause
