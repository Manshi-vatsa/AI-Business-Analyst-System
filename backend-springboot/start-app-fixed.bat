@echo off
set JAVA_HOME=C:\Progra~1\Java\jdk-17
set PATH=%JAVA_HOME%\bin;%PATH%
echo Starting Spring Boot application with Java 17...
java -version
.\mvnw.cmd spring-boot:run
