@echo off
echo Starting Spring Boot Backend - Final Version...

rem Use quotes for paths with spaces
set "JAVA_EXE=C:\Program Files\Java\jdk-22\bin\java.exe"

rem Test Java
echo Testing Java...
"%JAVA_EXE%" -version

cd /d "D:\AI_Business_Analyst_System\backend-springboot"

rem Try to build with direct Java path
echo Building project...
"%JAVA_EXE%" -cp ".\mvnw\wrapper\maven-wrapper.jar" org.apache.maven.wrapper.MavenWrapperMain clean package -DskipTests

if exist "target\*.jar" (
    echo Starting from JAR file...
    for %%f in (target\*.jar) do (
        echo Running: %%f
        "%JAVA_EXE%" -jar "%%f"
        goto :end
    )
) else (
    echo No JAR file found
    echo Trying to run with Maven wrapper...
    .\mvnw spring-boot:run
)

:end
pause
