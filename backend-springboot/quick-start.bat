@echo off
set JAVA_HOME=C:\Program Files\Java\jdk-17
set PATH=%JAVA_HOME%\bin;%PATH%
echo Using Java 17
java -version
echo.
echo Starting Spring Boot application...
java -jar target\classes -cp "C:\Users\MANSHI~1\.m2\repository\org\springframework\boot\spring-boot\3.2.5\spring-boot-3.2.5.jar" com.ai.analytics.AiAnalyticsApplication
