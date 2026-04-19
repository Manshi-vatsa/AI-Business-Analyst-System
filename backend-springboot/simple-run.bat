@echo off
set JAVA_HOME=C:\Program Files\Java\jdk-17
set PATH=%JAVA_HOME%\bin;%PATH%
echo Using Java 17...
java -version
echo.
echo Starting Spring Boot...
java -Dspring.profiles.active=dev -jar "C:\Users\MANSHI~1\.m2\repository\org\springframework\boot\spring-boot-devtools\3.2.5\spring-boot-devtools-3.2.5.jar;C:\Users\MANSHI~1\.m2\repository\org\springframework\boot\spring-boot\3.2.5\spring-boot-3.2.5.jar" -cp "target/classes" com.ai.analytics.AiAnalyticsApplication
