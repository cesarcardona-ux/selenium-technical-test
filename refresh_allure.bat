@echo off
REM ============================================
REM Script: Refresh Allure Report
REM ============================================
REM Este script regenera el reporte de Allure
REM con los últimos resultados de tests.
REM
REM Uso: Doble click después de ejecutar tests
REM ============================================

echo.
echo ========================================
echo   Refreshing Allure Report...
echo ========================================
echo.

REM Verificar que existan resultados
if not exist "reports\allure" (
    echo ERROR: No test results found in reports\allure
    echo Please run tests first.
    pause
    exit /b 1
)

REM Regenerar el reporte HTML desde los resultados JSON
echo Generating HTML report...
allure generate reports\allure -o reports\allure-report --clean 2>&1

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   SUCCESS! Report updated.
    echo ========================================
    echo.
    echo Press F5 in your browser to see the new tests!
    echo Server URL: http://localhost:8000
    echo.
) else (
    echo.
    echo ========================================
    echo   ERROR: Failed to generate report
    echo ========================================
    echo.
    echo Check if Allure is installed correctly.
    echo.
)

pause
