@echo off
echo Starting Spring Boot with Maven...

rem Set Java path
set JAVA_HOME=C:\Program Files\Java\jdk-17
set PATH=%JAVA_HOME%\bin;%PATH%

cd /d "D:\AI_Business_Analyst_System\backend-springboot"

echo Java version:
java -version

echo.
echo Building project...
call .\mvnw clean package -DskipTests

if exist "target\*.jar" (
    echo.
    echo Starting Spring Boot from JAR...
    for %%f in (target\*.jar) do (
        java -jar "%%f"
        goto :end
    )
) else (
    echo.
    echo No JAR file found, trying to run directly...
    call .\mvnw spring-boot:run
)

:end
pause
