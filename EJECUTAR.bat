@echo off
REM ====================================
REM Budget Converter - Ejecutar Windows
REM ====================================

echo.
echo ========================================
echo   Budget Converter
echo ========================================
echo.
echo Iniciando aplicacion...
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo Docs API: http://localhost:8000/docs
echo.
echo Presiona Ctrl+C para detener
echo ========================================
echo.

REM Iniciar Backend
start "Budget Converter - Backend" cmd /k "cd backend && venv\Scripts\activate.bat && python -m app.main"

REM Esperar 5 segundos
timeout /t 5 /nobreak >nul

REM Iniciar Frontend
start "Budget Converter - Frontend" cmd /k "cd frontend && npm run dev"

REM Esperar 3 segundos mas
timeout /t 3 /nobreak >nul

REM Abrir navegador
start http://localhost:3000

echo.
echo La aplicacion se esta iniciando...
echo Se abrira automaticamente en tu navegador
echo.
echo Para DETENER la aplicacion:
echo - Cierra las ventanas de Backend y Frontend
echo.
pause
