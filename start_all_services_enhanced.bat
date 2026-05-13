@echo off
echo ==========================================
echo Starting Enhanced AI Business Analyst System
echo ==========================================
echo.

echo [1/3] Starting FastAPI Service (Port 8000)...
cd /d "%~dp0ai-python-service"
start "FastAPI Service" cmd /k "echo FastAPI Service running... & python main.py"

echo.
echo [2/3] Waiting for FastAPI to start...
timeout /t 10 /nobreak >nul

echo [3/3] Starting Spring Boot Service (Port 8080)...
cd /d "%~dp0backend-springboot"
start "Spring Boot Service" cmd /k "echo Spring Boot Service running... & ./mvnw spring-boot:run"

echo.
echo ==========================================
echo Services Starting Up...
echo ==========================================
echo.
echo FastAPI: http://localhost:8000
echo Spring Boot: http://localhost:8080
echo.
echo Testing script: python test_springboot_fastapi.py
echo.
echo Wait 30-60 seconds for services to fully start before testing.
pause
