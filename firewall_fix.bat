@echo off
echo ==========================================
echo Adding Windows Firewall Rule for Port 8000
echo ==========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script requires administrator privileges
    echo Please right-click and "Run as administrator"
    pause
    exit /b 1
)

echo Adding firewall rule for port 8000...
netsh advfirewall firewall add rule name="Allow Port 8000" dir=in action=allow protocol=TCP localport=8000

if %errorLevel% equ 0 (
    echo SUCCESS: Firewall rule added successfully
) else (
    echo ERROR: Failed to add firewall rule
)

echo.
echo Checking firewall rules...
netsh advfirewall firewall show rule name="Allow Port 8000"

echo.
echo ==========================================
echo Firewall configuration complete
echo ==========================================
pause
