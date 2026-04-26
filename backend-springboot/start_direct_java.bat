@echo off
echo ========================================
echo DIRECT JAVA STARTUP SOLUTION
echo ========================================

echo.
echo 1. Finding Java installation...
for /f "tokens=*" %%i in ('dir /b /ad "C:\Program Files\Java\jdk*" 2^>nul') do (
    set JAVA_PATH=C:\Program Files\Java\%%i\bin\java.exe
    echo Found Java: %%i
    goto :found_java
)

echo Java not found
pause
exit /b 1

:found_java
echo Java Path: %JAVA_PATH%

echo.
echo 2. Testing Java...
"%JAVA_PATH%" -version

echo.
echo 3. Changing to backend directory...
cd /d "D:\AI_Business_Analyst_System\backend-springboot"

echo.
echo 4. Starting Spring Boot with Direct Java...
echo Using Maven wrapper with direct Java path...
"%JAVA_PATH%" -cp ".\mvnw\wrapper\maven-wrapper.jar" org.apache.maven.wrapper.MavenWrapperMain spring-boot:run

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ SUCCESS: Spring Boot started!
    echo.
    echo 5. Testing connection...
    timeout /t 15 /nobreak > nul
    
    echo Testing health endpoint...
    curl -s http://localhost:8080/ai/health && (
        echo ✅ Health check PASSED
        echo Spring Boot URL: http://localhost:8080
        echo Health Endpoint: http://localhost:8080/ai/health
        echo.
        echo Android app should connect to: http://192.168.29.53:8080
    ) || (
        echo ⚠️ Health check failed - Spring Boot may still be starting
        echo Please wait 30 seconds for full startup
    )
) else (
    echo.
    echo ❌ FAILED: Spring Boot failed to start
    echo Error code: %ERRORLEVEL%
    echo.
    echo Please check:
    echo 1. Java installation
    echo 2. Maven wrapper files
    echo 3. Project configuration
)

echo.
echo ========================================
echo STARTUP COMPLETE
echo ========================================
pause
