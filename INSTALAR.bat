@echo off
REM ====================================
REM Budget Converter - Instalador Windows
REM ====================================

echo.
echo ========================================
echo   Budget Converter - Instalador
echo ========================================
echo.

REM Verificar Python
echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo Descargalo de: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo Python encontrado OK

REM Verificar Node.js
echo [2/4] Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js no esta instalado
    echo Descargalo de: https://nodejs.org/
    echo.
    pause
    exit /b 1
)
echo Node.js encontrado OK

REM Instalar backend
echo [3/4] Instalando Backend...
cd backend
if not exist venv (
    echo Creando entorno virtual...
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
if not exist .env (
    copy .env.example .env
    echo.
    echo IMPORTANTE: Edita backend\.env y anade tu ANTHROPIC_API_KEY
    echo.
)
cd ..

REM Instalar frontend
echo [4/4] Instalando Frontend...
cd frontend
call npm install
cd ..

echo.
echo ========================================
echo   Instalacion Completada!
echo ========================================
echo.
echo Siguiente paso:
echo 1. Edita backend\.env con tu ANTHROPIC_API_KEY
echo 2. Haz doble clic en: EJECUTAR.bat
echo.
pause
