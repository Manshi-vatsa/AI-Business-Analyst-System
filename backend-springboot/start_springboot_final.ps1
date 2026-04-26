# PowerShell script to start Spring Boot with proper Java handling
Write-Host "Starting Spring Boot Backend..." -ForegroundColor Green

# Set Java environment properly
$javaPath = "C:\Program Files\Java\jdk-22\bin\java.exe"
$env:JAVA_HOME = "C:\Program Files\Java\jdk-22"
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"

Write-Host "Java path: $javaPath" -ForegroundColor Yellow
Write-Host "JAVA_HOME: $env:JAVA_HOME" -ForegroundColor Yellow

# Test Java
try {
    $javaVersion = & $javaPath -version 2>&1
    Write-Host "✅ Java test passed" -ForegroundColor Green
} catch {
    Write-Host "❌ Java test failed: $_" -ForegroundColor Red
    exit 1
}

# Change to backend directory
Set-Location "D:\AI_Business_Analyst_System\backend-springboot"

# Try to start Spring Boot
Write-Host "🚀 Starting Spring Boot..." -ForegroundColor Blue
try {
    # Set environment variables for Maven wrapper
    $env:JAVA_HOME = "C:\Program Files\Java\jdk-22"
    $env:PATH = "$env:JAVA_HOME\bin;$env:PATH"
    
    # Start Spring Boot
    & .\mvnw spring-boot:run
    
} catch {
    Write-Host "❌ Failed to start Spring Boot: $_" -ForegroundColor Red
    
    # Try alternative approach
    Write-Host "🔄 Trying alternative approach..." -ForegroundColor Yellow
    
    # Try to build and run from JAR
    try {
        & .\mvnw clean package -DskipTests
        
        $jarFiles = Get-ChildItem "target\*.jar" -ErrorAction SilentlyContinue
        if ($jarFiles.Count -gt 0) {
            $jarFile = $jarFiles | Select-Object -First 1
            Write-Host "📦 Running from JAR: $($jarFile.Name)" -ForegroundColor Green
            & $javaPath -jar $jarFile.FullName
        } else {
            Write-Host "❌ No JAR file found" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Build failed: $_" -ForegroundColor Red
    }
}

Write-Host "Spring Boot startup completed" -ForegroundColor Green
