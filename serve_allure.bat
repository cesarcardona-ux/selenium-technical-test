@echo off
REM ============================================
REM Script: Serve Allure Report (Simple)
REM ============================================
REM Este script levanta un servidor HTTP para
REM ver el reporte de Allure que ya está generado.
REM ============================================

echo.
echo ========================================
echo   Starting Allure Report Server...
echo ========================================
echo.
echo Server: http://localhost:8000
echo.
echo IMPORTANT: Keep this window OPEN
echo Press Ctrl+C to stop the server
echo.
echo Opening browser in 3 seconds...
echo ========================================
echo.

REM Abrir navegador después de 3 segundos
start "" powershell -WindowStyle Hidden -Command "Start-Sleep -Seconds 3; Start-Process 'http://localhost:8000'"

REM Cambiar a directorio del reporte
cd reports\allure-report

REM Iniciar servidor HTTP
python -m http.server 8000
