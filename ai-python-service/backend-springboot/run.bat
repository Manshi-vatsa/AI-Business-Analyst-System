@echo off
set JAVA_HOME=C:\Program Files\Java\jdk-17
set PATH=%JAVA_HOME%\bin;%PATH%
echo Starting Spring Boot with Java 17...
java -version
echo.
echo Starting application...
java -cp "target/classes;C:\Users\MANSHI~1\.m2\repository\org\springframework\boot\spring-boot\3.2.5\spring-boot-3.2.5.jar" org.springframework.boot.loader.JarLauncher -jar "C:\Users\MANSHI~1\.m2\repository\org\springframework\boot\spring-boot-loader-tools\3.2.5\spring-boot-loader-tools-3.2.5.jar" --scan "target/classes"
