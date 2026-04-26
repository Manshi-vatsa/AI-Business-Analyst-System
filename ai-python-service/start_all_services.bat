@echo off
echo ========================================
echo Starting AI Business Analyst System
echo ========================================

echo.
echo 1. Starting Spring Boot Backend...
cd /d "D:\AI_Business_Analyst_System\backend-springboot"

rem Try to find Java installation automatically
for /f "tokens=*" %%i in ('dir /b "C:\Program Files\Java\jdk*" 2^>nul') do (
    set JAVA_HOME=C:\Program Files\Java\%%i
    echo Found Java: %%i
    goto :found_java
)

echo Java not found in standard location
echo Please ensure Java is installed
pause
exit /b 1

:found_java
set PATH=%JAVA_HOME%\bin;%PATH%

echo Java version:
java -version

echo.
echo Starting Spring Boot...
start "Spring Boot" cmd /k ".\mvnw spring-boot:run"

echo.
echo 2. Starting Python FastAPI...
cd /d "D:\AI_Business_Analyst_System\ai-python-service"
start "Python FastAPI" cmd /k ".\.venv\Scripts\python main.py"

echo.
echo 3. Waiting for services to start...
timeout /t 10 /nobreak

echo.
echo 4. Testing connectivity...
echo Testing Spring Boot...
curl -s http://localhost:8080/ai/health || echo Spring Boot not ready yet

echo Testing Python FastAPI...
curl -s http://localhost:8000/health || echo Python FastAPI not ready yet

echo.
echo ========================================
echo Services started!
echo ========================================
echo Spring Boot: http://localhost:8080
echo Python FastAPI: http://localhost:8000
echo.
echo Android app should connect to: http://192.168.29.53:8080
echo.
echo Press any key to exit...
pause
