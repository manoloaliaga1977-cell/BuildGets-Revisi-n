#!/bin/bash
# Script para iniciar toda la aplicación

echo "🏗️  Budget Converter - Iniciando aplicación completa"
echo "======================================================"
echo ""

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Iniciar backend
echo "🔧 Iniciando Backend..."
cd backend
chmod +x run.sh
./run.sh &
BACKEND_PID=$!
cd ..

# Esperar a que el backend inicie
echo "⏳ Esperando al backend..."
sleep 5

# Iniciar frontend
echo "🎨 Iniciando Frontend..."
cd frontend
chmod +x run.sh
./run.sh &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Aplicación iniciada correctamente!"
echo "======================================================"
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo "======================================================"
echo ""
echo "Presiona Ctrl+C para detener todos los servicios"
echo ""

# Esperar indefinidamente
wait
