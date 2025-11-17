#!/bin/bash
# ====================================
# Budget Converter - Ejecutar Mac/Linux
# ====================================

clear
echo ""
echo "========================================"
echo "  Budget Converter"
echo "========================================"
echo ""
echo "Iniciando aplicación..."
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "Docs API: http://localhost:8000/docs"
echo ""
echo "Presiona Ctrl+C para detener"
echo "========================================"
echo ""

# Función para limpiar al salir
cleanup() {
    echo ""
    echo "Deteniendo servicios..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Iniciar Backend
cd backend
source venv/bin/activate
python -m app.main &
BACKEND_PID=$!
cd ..

# Esperar 5 segundos
sleep 5

# Iniciar Frontend
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Esperar 3 segundos
sleep 3

# Abrir navegador
if command -v open &> /dev/null; then
    # macOS
    open http://localhost:3000
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open http://localhost:3000
fi

echo ""
echo "✅ La aplicación está ejecutándose"
echo "Se abrirá automáticamente en tu navegador"
echo ""
echo "Para DETENER: Presiona Ctrl+C"
echo ""

# Esperar
wait
