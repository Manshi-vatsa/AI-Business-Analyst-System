# PowerShell script to start Spring Boot backend with proper Java configuration
Write-Host "=== Starting AI Business Analyst Backend ===" -ForegroundColor Green

# Find and set Java installation
$javaDirs = Get-ChildItem "C:\Program Files\Java" -Directory | Where-Object { $_.Name -like "jdk*" }
if ($javaDirs.Count -eq 0) {
    Write-Host "❌ No Java installation found in C:\Program Files\Java" -ForegroundColor Red
    Write-Host "Please install Java JDK first" -ForegroundColor Yellow
    exit 1
}

$latestJava = $javaDirs | Sort-Object Name -Descending | Select-Object -First 1
$env:JAVA_HOME = $latestJava.FullName
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"

Write-Host "✅ Java found: $($latestJava.Name)" -ForegroundColor Green
Write-Host "✅ JAVA_HOME: $env:JAVA_HOME" -ForegroundColor Green

# Test Java
try {
    $javaVersion = java -version 2>&1
    Write-Host "✅ Java version check passed" -ForegroundColor Green
} catch {
    Write-Host "❌ Java version check failed: $_" -ForegroundColor Red
    exit 1
}

# Change to backend directory
Set-Location "D:\AI_Business_Analyst_System\backend-springboot"
Write-Host "📁 Changed to backend directory" -ForegroundColor Blue

# Check if Maven wrapper exists
if (-not (Test-Path ".\mvnw")) {
    Write-Host "❌ Maven wrapper not found" -ForegroundColor Red
    exit 1
}

# Try to start Spring Boot
Write-Host "🚀 Starting Spring Boot backend..." -ForegroundColor Blue
try {
    # First try to build
    Write-Host "📦 Building project..." -ForegroundColor Yellow
    $buildResult = & .\mvnw clean package -DskipTests
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Build failed, trying to run directly..." -ForegroundColor Yellow
    }
    
    # Try to run
    Write-Host "🏃 Starting application..." -ForegroundColor Yellow
    & .\mvnw spring-boot:run
    
} catch {
    Write-Host "❌ Failed to start Spring Boot: $_" -ForegroundColor Red
    
    # Try alternative approach - run from JAR
    $jarFiles = Get-ChildItem "target\*.jar" -ErrorAction SilentlyContinue
    if ($jarFiles.Count -gt 0) {
        Write-Host "🔄 Trying to run from JAR file..." -ForegroundColor Yellow
        $jarFile = $jarFiles | Select-Object -First 1
        java -jar $jarFile.FullName
    } else {
        Write-Host "❌ No JAR file found. Please build the project first." -ForegroundColor Red
        Write-Host "Run: .\mvnw clean package -DskipTests" -ForegroundColor Yellow
    }
}

Write-Host "=== Backend startup completed ===" -ForegroundColor Green
