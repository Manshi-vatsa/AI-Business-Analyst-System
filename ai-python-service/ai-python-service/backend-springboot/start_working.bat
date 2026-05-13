@echo off
echo Starting Spring Boot Backend - Working Solution...

rem Find Java installation automatically
for /f "tokens=*" %%i in ('dir /b /ad "C:\Program Files\Java\jdk*" 2^>nul') do (
    set JAVA_PATH=C:\Program Files\Java\%%i\bin
    echo Found Java at: %%i
    goto :found_java
)

echo Java not found
pause
exit /b 1

:found_java
echo Using Java: %JAVA_PATH%

cd /d "D:\AI_Business_Analyst_System\backend-springboot"

rem Test Java
echo Testing Java...
"%JAVA_PATH%\java.exe" -version

rem Try to start Spring Boot
echo Starting Spring Boot...
"%JAVA_PATH%\java.exe" -cp ".\mvnw\wrapper\maven-wrapper.jar" org.apache.maven.wrapper.MavenWrapperMain spring-boot:run

pause
