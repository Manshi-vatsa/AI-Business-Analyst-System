@echo off
echo ========================================
echo ULTIMATE BACKEND FIX SOLUTION
echo ========================================

echo.
echo 1. Finding Java installation...
for /f "tokens=*" %%i in ('dir /b /ad "C:\Program Files\Java\jdk*" 2^>nul') do (
    set JAVA_PATH=C:\Program Files\Java\%%i\bin
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
"%JAVA_PATH%\java.exe" -version

echo.
echo 3. Changing to backend directory...
cd /d "D:\AI_Business_Analyst_System\backend-springboot"

echo.
echo 4. Starting Spring Boot - Multiple Methods...
echo.
echo Method 1: Direct Java with Maven Wrapper...
set JAVA_HOME=C:\Program Files\Java\jdk-17
set PATH=%JAVA_HOME%\bin;%PATH%
call .\mvnw spring-boot:run

if %ERRORLEVEL% EQU 0 (
    echo ✅ SUCCESS: Spring Boot started with Method 1
    goto :test_connection
)

echo.
echo Method 2: Build and Run JAR...
echo Building project...
call .\mvnw clean package -DskipTests

if exist "target\*.jar" (
    echo Starting from JAR file...
    for %%f in (target\*.jar) do (
        "%JAVA_PATH%\java.exe" -jar "%%f"
        echo ✅ SUCCESS: Spring Boot started with Method 2
        goto :test_connection
    )
)

echo.
echo Method 3: Try with different Java version...
set JAVA_HOME=C:\Program Files\Java\jdk-22
set PATH=%JAVA_HOME%\bin;%PATH%
call .\mvnw spring-boot:run

if %ERRORLEVEL% EQU 0 (
    echo ✅ SUCCESS: Spring Boot started with Method 3
    goto :test_connection
)

echo.
echo ❌ All methods failed
echo Please check:
echo 1. Java installation
echo 2. Maven wrapper files
echo 3. Project configuration
goto :end

:test_connection
echo.
echo 5. Testing connection...
timeout /t 10 /nobreak > nul
curl -s http://localhost:8080/ai/health && (
    echo ✅ Connection test PASSED
    echo Spring Boot URL: http://localhost:8080
    echo Health Endpoint: http://localhost:8080/ai/health
) || (
    echo ⚠️ Connection test failed - Spring Boot may still be starting
    echo Please wait 30 seconds for full startup
)

echo.
echo ========================================
echo BACKEND STARTUP COMPLETE
echo ========================================
echo.
echo Next Steps:
echo 1. Test Android app connection
echo 2. Build and install Android APK
echo 3. Monitor logs for connection status
echo.

:end
pause
