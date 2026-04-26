Write-Host "Starting Spring Boot Backend..." -ForegroundColor Green

# Set Java environment
$env:JAVA_HOME = "C:\Program Files\Java\jdk-22"
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"

# Change to backend directory
Set-Location "D:\AI_Business_Analyst_System\backend-springboot"

# Test Java
try {
    $javaVersion = java -version 2>&1
    Write-Host "✅ Java test passed" -ForegroundColor Green
} catch {
    Write-Host "❌ Java test failed: $_" -ForegroundColor Red
    exit 1
}

# Start Spring Boot
Write-Host "🚀 Starting Spring Boot..." -ForegroundColor Blue
try {
    & .\mvnw spring-boot:run
} catch {
    Write-Host "❌ Failed to start Spring Boot: $_" -ForegroundColor Red
    Write-Host "Trying alternative approach..." -ForegroundColor Yellow
    
    # Try to build and run from JAR
    try {
        & .\mvnw clean package -DskipTests
        
        $jarFiles = Get-ChildItem "target\*.jar" -ErrorAction SilentlyContinue
        if ($jarFiles.Count -gt 0) {
            $jarFile = $jarFiles | Select-Object -First 1
            Write-Host "📦 Running from JAR: $($jarFile.Name)" -ForegroundColor Green
            java -jar $jarFile.FullName
        } else {
            Write-Host "❌ No JAR file found" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Build failed: $_" -ForegroundColor Red
    }
}
