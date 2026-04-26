@echo off
echo Starting Spring Boot Backend...

rem Find Java automatically
for /f "tokens=*" %%i in ('dir /b /ad "C:\Program Files\Java\jdk*" 2^>nul') do (
    set "JAVA_HOME=C:\Program Files\Java\%%i"
    echo Found Java: %%i
    goto :found_java
)

echo Java not found
pause
exit /b 1

:found_java
echo JAVA_HOME: %JAVA_HOME%
set "PATH=%JAVA_HOME%\bin;%PATH%"

cd /d "D:\AI_Business_Analyst_System\backend-springboot"

echo Testing Java...
java -version

echo Starting Spring Boot...
.\mvnw spring-boot:run

pause
