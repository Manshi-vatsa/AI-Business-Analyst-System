# PowerShell script to start Spring Boot backend
Write-Host "Starting Spring Boot Backend..."

# Set Java environment
$env:JAVA_HOME = "C:\Program Files\Java\jdk-17.0.12"
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"

# Change to backend directory
Set-Location "D:\AI_Business_Analyst_System\backend-springboot"

Write-Host "Java version:"
java -version

Write-Host "Starting Spring Boot..."
# Try to start with Maven
try {
    .\mvnw spring-boot:run
} catch {
    Write-Host "Maven startup failed, trying alternative approach..."
    # Try with java directly
    if (Test-Path "target\*.jar") {
        $jarFile = Get-ChildItem "target\*.jar" | Select-Object -First 1
        Write-Host "Starting with JAR file: $($jarFile.Name)"
        java -jar $jarFile.FullName
    } else {
        Write-Host "No JAR file found. Please build the project first."
        Write-Host "Run: .\mvnw clean package"
    }
}
