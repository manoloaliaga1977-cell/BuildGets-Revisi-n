#!/usr/bin/env python3
"""
Script simple para iniciar el servidor
Detecta automáticamente el puerto según la plataforma
"""
import os
import sys

# Detectar plataforma
def detect_platform():
    if 'REPL_ID' in os.environ:
        return 'replit'
    elif 'RAILWAY_ENVIRONMENT' in os.environ:
        return 'railway'
    elif 'RENDER' in os.environ:
        return 'render'
    elif 'CODESPACE_NAME' in os.environ:
        return 'codespaces'
    else:
        return 'local'

# Configurar según plataforma
platform = detect_platform()
print(f"🌐 Plataforma detectada: {platform}")

# Configurar puerto
if platform == 'replit':
    port = int(os.getenv('PORT', 8000))
    host = '0.0.0.0'
elif platform == 'railway' or platform == 'render':
    port = int(os.getenv('PORT', 8000))
    host = '0.0.0.0'
elif platform == 'codespaces':
    port = 8000
    host = '0.0.0.0'
else:  # local
    port = int(os.getenv('API_PORT', 8000))
    host = os.getenv('API_HOST', '127.0.0.1')

print(f"🚀 Iniciando servidor en {host}:{port}")
print(f"📚 Docs disponibles en: http://{host}:{port}/docs")
print()

# Iniciar servidor
if __name__ == "__main__":
    import uvicorn

    # Cargar variables de entorno
    from dotenv import load_dotenv
    load_dotenv()

    # Verificar API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key and not api_key.startswith('your_'):
        print("✅ ANTHROPIC_API_KEY configurada - Funciones de IA habilitadas")
    else:
        print("⚠️  ANTHROPIC_API_KEY no configurada - Funciones de IA deshabilitadas")
        print("   (BC3→PDF y BC3→JSON funcionarán, PDF→BC3 requiere IA)")
    print()

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=platform == 'local',  # Solo reload en local
        log_level="info"
    )
