@echo off
echo ========================================
echo FINAL BACKEND STARTUP SOLUTION
echo ========================================

echo.
echo 1. Finding Java installation...
for /f "tokens=*" %%i in ('dir /b /ad "C:\Program Files\Java\jdk*" 2^>nul') do (
    set JAVA_PATH=C:\Program Files\Java\%%i\bin
    echo Found Java: %%i
    goto :found_java
)

echo Java not found in standard location
echo Please install Java JDK first
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
echo 4. Starting Spring Boot...
echo Method A: Direct Maven Wrapper
call .\mvnw spring-boot:run

if %ERRORLEVEL% EQU 0 (
    echo ✅ Spring Boot started successfully!
    goto :success
)

echo.
echo Method B: Build and Run JAR
echo Building project...
call .\mvnw clean package -DskipTests

if exist "target\*.jar" (
    echo Starting from JAR file...
    for %%f in (target\*.jar) do (
        "%JAVA_PATH%\java.exe" -jar "%%f"
        goto :success
    )
)

echo.
echo ❌ All methods failed
echo Please check:
echo 1. Java installation
echo 2. Maven wrapper files
echo 3. Project configuration
pause
exit /b 1

:success
echo.
echo ========================================
echo Spring Boot is running!
echo ========================================
echo Testing connection...
timeout /t 5 /nobreak > nul
curl -s http://localhost:8080/ai/health || echo Spring Boot may still be starting...
echo.
echo Expected URL: http://localhost:8080
echo Expected Health: http://localhost:8080/ai/health
echo.
echo Press any key to exit...
pause
