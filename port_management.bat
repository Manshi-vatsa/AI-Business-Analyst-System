@echo off
echo ==========================================
echo PORT MANAGEMENT UTILITIES
echo ==========================================
echo.

:menu
echo 1. Find process using port 8000
echo 2. Kill process using port 8000
echo 3. Find process using port 8080
echo 4. Kill process using port 8080
echo 5. Check all listening ports
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto find8000
if "%choice%"=="2" goto kill8000
if "%choice%"=="3" goto find8080
if "%choice%"=="4" goto kill8080
if "%choice%"=="5" goto checkall
if "%choice%"=="6" goto exit
goto menu

:find8000
echo.
echo Finding process using port 8000...
netstat -ano | findstr :8000
echo.
pause
goto menu

:kill8000
echo.
echo Finding process using port 8000...
for /f "tokens=5" %%i in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Found PID: %%i
    echo Killing process...
    taskkill /PID %%i /F
)
if not found (
    echo No process found using port 8000
)
echo.
pause
goto menu

:find8080
echo.
echo Finding process using port 8080...
netstat -ano | findstr :8080
echo.
pause
goto menu

:kill8080
echo.
echo Finding process using port 8080...
for /f "tokens=5" %%i in ('netstat -ano ^| findstr :8080 ^| findstr LISTENING') do (
    echo Found PID: %%i
    echo Killing process...
    taskkill /PID %%i /F
)
if not found (
    echo No process found using port 8080
)
echo.
pause
goto menu

:checkall
echo.
echo Checking all listening ports...
netstat -ano | findstr LISTENING
echo.
pause
goto menu

:exit
echo.
echo Port management complete.
pause
