@echo off
echo Fixing Java path and starting backend...

rem Find Java installation
for /f "tokens=*" %%i in ('dir /b /ad "C:\Program Files\Java\jdk*" 2^>nul') do (
    set JAVA_HOME=C:\Program Files\Java\%%i
    echo Found Java: %%i
    goto :found_java
)

echo Java not found in standard location
pause
exit /b 1

:found_java
echo JAVA_HOME: %JAVA_HOME%
echo Adding Java to PATH...
set PATH=%JAVA_HOME%\bin;%PATH%

echo Testing Java...
java -version

echo Starting Spring Boot backend...
cd /d "D:\AI_Business_Analyst_System\backend-springboot"

rem Try to start with Maven
echo Starting with Maven...
.\mvnw spring-boot:run

pause
