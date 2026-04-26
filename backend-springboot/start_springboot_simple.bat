@echo off
echo Starting Spring Boot Backend - Simple Approach...

rem Set Java path
set JAVA_PATH="C:\Program Files\Java\jdk-22\bin\java.exe"

rem Test Java
echo Testing Java...
"%JAVA_PATH%" -version

cd /d "D:\AI_Business_Analyst_System\backend-springboot"

rem Try to run directly with Maven wrapper
echo Starting Spring Boot...
set JAVA_HOME=C:\Program Files\Java\jdk-22
.\mvnw spring-boot:run

pause
