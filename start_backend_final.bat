@echo off
echo ========================================
echo Starting AI Business Analyst Backend
echo ========================================

echo.
echo 1. Setting up Java environment...
set JAVA_HOME=C:\Program Files\Java\jdk-22
set PATH=%JAVA_HOME%\bin;%PATH%

echo Java version:
java -version

echo.
echo 2. Starting Spring Boot Backend...
cd /d "D:\AI_Business_Analyst_System\backend-springboot"

rem Try to start Spring Boot with Maven wrapper
echo Starting Spring Boot with Maven wrapper...
call .\mvnw spring-boot:run

pause
