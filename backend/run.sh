#!/bin/bash
# Script para ejecutar el backend

echo "🚀 Iniciando Budget Converter Backend..."

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo "📦 Activando entorno virtual..."
    source venv/bin/activate
else
    echo "⚠️  No se encontró entorno virtual. Créalo con: python -m venv venv"
    exit 1
fi

# Verificar que las dependencias estén instaladas
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📥 Instalando dependencias..."
    pip install -r requirements.txt
fi

# Verificar que exista el archivo .env
if [ ! -f ".env" ]; then
    echo "⚠️  Archivo .env no encontrado. Creando desde .env.example..."
    cp .env.example .env
    echo "⚠️  Por favor edita .env y añade tu ANTHROPIC_API_KEY"
fi

# Ejecutar la aplicación
echo "✅ Iniciando servidor en http://localhost:8000"
echo "📚 Documentación disponible en http://localhost:8000/docs"
echo ""

python -m app.main
