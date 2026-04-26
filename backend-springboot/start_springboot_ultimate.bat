@echo off
echo ========================================
echo ULTIMATE SPRING BOOT STARTUP
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
echo 4. Starting Spring Boot - Multiple Methods...

rem Method 1: Direct Maven with explicit classpath
echo Method 1: Direct Maven execution...
"%JAVA_PATH%" -cp ".\mvnw\wrapper\maven-wrapper.jar" org.apache.maven.wrapper.MavenWrapperMain spring-boot:run

if %ERRORLEVEL% EQU 0 (
    echo ✅ SUCCESS: Spring Boot started with Method 1!
    goto :test_connection
)

echo.
echo Method 2: Build and Run JAR
echo Building project...
"%JAVA_PATH%" -cp ".\mvnw\wrapper\maven-wrapper.jar" org.apache.maven.wrapper.MavenWrapperMain clean package -DskipTests

if exist "target\*.jar" (
    echo Starting from JAR file...
    for %%f in (target\*.jar) do (
        "%JAVA_PATH%" -jar "%%f"
        echo ✅ SUCCESS: Spring Boot started with Method 2!
        goto :test_connection
    )
)

echo.
echo Method 3: Try with different Java version
for /f "tokens=*" %%j in ('dir /b /ad "C:\Program Files\Java\jdk*" 2^>nul') do (
    if not "%%j"=="jdk-17" (
        echo Trying with Java %%j...
        set ALT_JAVA_PATH=C:\Program Files\Java\%%j\bin\java.exe
        "%ALT_JAVA_PATH%" -cp ".\mvnw\wrapper\maven-wrapper.jar" org.apache.maven.wrapper.MavenWrapperMain spring-boot:run
        if !ERRORLEVEL! EQU 0 (
            echo ✅ SUCCESS: Spring Boot started with Method 3!
            goto :test_connection
        )
    )
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

echo Testing health endpoint...
curl -s http://localhost:8080/ai/health && (
    echo ✅ Connection test PASSED
    echo Spring Boot URL: http://localhost:8080
    echo Health Endpoint: http://localhost:8080/ai/health
    echo Android app should connect to: http://192.168.29.53:8080
) || (
    echo ⚠️ Connection test failed - Spring Boot may still be starting
    echo Please wait 30 seconds for full startup
)

echo.
echo ========================================
echo STARTUP COMPLETE
echo ========================================
echo.
echo Expected URLs:
echo - Spring Boot: http://localhost:8080
echo - Health Check: http://localhost:8080/ai/health
echo - Android App: http://192.168.29.53:8080
echo.

:end
pause
