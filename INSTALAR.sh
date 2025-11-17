#!/bin/bash
# ====================================
# Budget Converter - Instalador Mac/Linux
# ====================================

clear
echo ""
echo "========================================"
echo "  Budget Converter - Instalador"
echo "========================================"
echo ""

# Verificar Python
echo "[1/4] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python no está instalado"
    echo "Instálalo desde: https://www.python.org/downloads/"
    echo ""
    read -p "Presiona Enter para salir..."
    exit 1
fi
echo "✅ Python encontrado OK"

# Verificar Node.js
echo "[2/4] Verificando Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ ERROR: Node.js no está instalado"
    echo "Instálalo desde: https://nodejs.org/"
    echo ""
    read -p "Presiona Enter para salir..."
    exit 1
fi
echo "✅ Node.js encontrado OK"

# Instalar backend
echo "[3/4] Instalando Backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r requirements.txt
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANTE: Edita backend/.env y añade tu ANTHROPIC_API_KEY"
    echo ""
fi
cd ..

# Instalar frontend
echo "[4/4] Instalando Frontend..."
cd frontend
npm install
cd ..

echo ""
echo "========================================"
echo "  ✅ Instalación Completada!"
echo "========================================"
echo ""
echo "Siguiente paso:"
echo "1. Edita backend/.env con tu ANTHROPIC_API_KEY"
echo "2. Ejecuta: ./EJECUTAR.sh"
echo ""
read -p "Presiona Enter para continuar..."
