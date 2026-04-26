@echo off
echo Starting Spring Boot Backend...
cd /d "D:\AI_Business_Analyst_System\backend-springboot"

set JAVA_HOME=C:\Program Files\Java\jdk-17.0.12
set PATH=%JAVA_HOME%\bin;%PATH%

echo Java version:
java -version

echo Starting Spring Boot...
.\mvnw spring-boot:run
