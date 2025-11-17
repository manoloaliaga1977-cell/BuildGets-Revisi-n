#!/bin/bash
# Script para ejecutar el frontend

echo "🚀 Iniciando Budget Converter Frontend..."

# Verificar que node_modules existe
if [ ! -d "node_modules" ]; then
    echo "📥 Instalando dependencias..."
    npm install
fi

# Ejecutar la aplicación
echo "✅ Iniciando servidor en http://localhost:3000"
echo ""

npm run dev
