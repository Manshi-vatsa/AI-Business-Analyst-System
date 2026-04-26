@echo off
echo ========================================
echo FINAL WORKING SPRING BOOT STARTUP
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
echo Using Java directly without Maven wrapper...

rem Set environment variables
set JAVA_HOME=C:\Program Files\Java\jdk-17
set PATH=%JAVA_HOME%\bin;%PATH%

rem Try to run Spring Boot directly
echo Attempting to run Spring Boot...
java -cp target\classes com.ai.analytics.MinimalController

if %ERRORLEVEL% EQU 0 (
    echo ✅ SUCCESS: Spring Boot started directly!
    goto :test_connection
)

echo.
echo 5. Trying Maven wrapper method...
echo Attempting Maven wrapper...
call .\mvnw spring-boot:run

if %ERRORLEVEL% EQU 0 (
    echo ✅ SUCCESS: Spring Boot started with Maven wrapper!
    goto :test_connection
)

echo.
echo ❌ Both methods failed
echo Please check:
echo 1. Java installation
echo 2. Project structure
echo 3. Maven configuration
goto :end

:test_connection
echo.
echo 6. Testing connection...
timeout /t 15 /nobreak > nul

echo Testing health endpoint...
curl -s http://localhost:8080/ai/health && (
    echo ✅ Connection test PASSED
    echo Spring Boot URL: http://localhost:8080
    echo Health Endpoint: http://localhost:8080/ai/health
    echo Android app should connect to: http://192.168.29.53:8080
    goto :success
)

echo.
echo ⚠️ Connection test failed - Spring Boot may still be starting
echo Please wait 30 seconds for full startup
goto :end

:success
echo.
echo ========================================
echo SPRING BOOT STARTUP COMPLETE
echo ========================================
echo.
echo Expected URLs:
echo - Spring Boot: http://localhost:8080
echo - Health Check: http://localhost:8080/ai/health
echo - Android App: http://192.168.29.53:8080
echo.

:end
pause
