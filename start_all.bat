@echo off
echo ========================================
echo Starting AI Business Analyst System
echo ========================================

echo.
echo 1. Setting up Java environment...
set JAVA_HOME=C:\Program Files\Java\jdk-17
set PATH=%JAVA_HOME%\bin;%PATH%

echo Java version:
java -version

echo.
echo 2. Starting Spring Boot Backend...
cd /d "D:\AI_Business_Analyst_System\backend-springboot"
start "Spring Boot Backend" cmd /k "title Spring Boot Backend && echo Starting Spring Boot... && .\mvnw spring-boot:run"

echo.
echo 3. Starting Python FastAPI...
cd /d "D:\AI_Business_Analyst_System\ai-python-service"
start "Python FastAPI" cmd /k "title Python FastAPI && echo Starting Python FastAPI... && .\.venv\Scripts\python main.py"

echo.
echo 4. Waiting for services to start...
timeout /t 20 /nobreak

echo.
echo 5. Testing connectivity...
echo Testing Spring Boot...
curl -s http://localhost:8080/ai/health || echo Spring Boot not ready yet

echo.
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
