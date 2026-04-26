@echo off
echo Starting Spring Boot Backend directly...

rem Find Java installation and use direct path
for /f "tokens=*" %%i in ('dir /b /ad "C:\Program Files\Java\jdk*" 2^>nul') do (
    set "JAVA_PATH=C:\Program Files\Java\%%i\bin"
    echo Found Java at: %%i
    goto :found_java
)

echo Java not found
pause
exit /b 1

:found_java
echo Using Java from: %JAVA_PATH%

cd /d "D:\AI_Business_Analyst_System\backend-springboot"

rem Try to build first using direct Java
echo Building project...
"%JAVA_PATH%\java.exe" -cp ".\mvnw\wrapper\maven-wrapper.jar" org.apache.maven.wrapper.MavenWrapperMain clean package -DskipTests

if exist "target\*.jar" (
    echo Starting from JAR file...
    for %%f in (target\*.jar) do (
        "%JAVA_PATH%\java.exe" -jar "%%f"
        goto :end
    )
) else (
    echo No JAR file found, trying to run directly...
    echo Please run: mvn clean package -DskipTests first
)

:end
pause
