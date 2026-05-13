# 🔧 PORT MANAGEMENT COMMANDS

## 📋 QUICK COMMANDS

### Find Process Using Port 8000
```bash
# Windows Command Prompt
netstat -ano | findstr :8000

# PowerShell
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess
```

### Kill Process Using Port 8000
```bash
# Windows Command Prompt
for /f "tokens=5" %i in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /PID %i /F

# PowerShell
$process = Get-NetTCPConnection -LocalPort 8000 | Select-Object -ExpandProperty OwningProcess
Stop-Process -Id $process -Force
```

### Find Process Using Port 8080
```bash
# Windows Command Prompt
netstat -ano | findstr :8080

# PowerShell
Get-NetTCPConnection -LocalPort 8080 | Select-Object OwningProcess
```

### Kill Process Using Port 8080
```bash
# Windows Command Prompt
for /f "tokens=5" %i in ('netstat -ano ^| findstr :8080 ^| findstr LISTENING') do taskkill /PID %i /F

# PowerShell
$process = Get-NetTCPConnection -LocalPort 8080 | Select-Object -ExpandProperty OwningProcess
Stop-Process -Id $process -Force
```

## 🚀 AUTOMATED SCRIPT

### Use the Port Management Script
```bash
# Run the automated port management script
.\port_management.bat
```

This script provides:
1. Find process using port 8000
2. Kill process using port 8000
3. Find process using port 8080
4. Kill process using port 8080
5. Check all listening ports

## 🔍 TROUBLESHOOTING

### Port Already in Use Error
```bash
# Check what's using the port
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F

# Verify port is free
netstat -ano | findstr :8000
```

### Permission Denied Error
```bash
# Run as administrator
# Right-click Command Prompt/PowerShell and "Run as administrator"

# Or use the port_management.bat script
```

### Process Won't Die
```bash
# Force kill with multiple attempts
taskkill /PID <PID> /F /T
taskkill /PID <PID> /F

# Or use Process Explorer for stubborn processes
```

## 📊 PORT ASSIGNMENT

### Final Port Configuration
- **Spring Boot**: Port 8080
- **Python FastAPI**: Port 8000
- **Android**: Connects to Spring Boot on 8080
- **Spring Boot**: Connects to Python on 8000

### Architecture Flow
```
Android App (192.168.29.53:8080)
    ↓
Spring Boot (localhost:8080)
    ↓
Python FastAPI (localhost:8000)
    ↓
MySQL Database (localhost:3306)
```
