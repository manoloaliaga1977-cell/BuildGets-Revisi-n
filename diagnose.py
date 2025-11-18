#!/usr/bin/env python3
"""
Script de diagnóstico para Budget Converter
Verifica que todo esté configurado correctamente
"""
import sys
import os

print("=" * 60)
print(" DIAGNÓSTICO DE BUDGET CONVERTER")
print("=" * 60)
print()

# Lista de resultados
results = []

# 1. Verificar Python
print("1️⃣  Verificando Python...")
python_version = sys.version_info
if python_version >= (3, 9):
    print(f"   ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    results.append(("Python", True))
else:
    print(f"   ❌ Python {python_version.major}.{python_version.minor} (se requiere 3.9+)")
    results.append(("Python", False))

# 2. Verificar dependencias
print("\n2️⃣  Verificando dependencias...")
required_modules = [
    'fastapi',
    'uvicorn',
    'pydantic',
    'reportlab',
    'pdfplumber',
    'anthropic'
]

missing = []
for module in required_modules:
    try:
        __import__(module)
        print(f"   ✅ {module}")
    except ImportError:
        print(f"   ❌ {module} (falta)")
        missing.append(module)

results.append(("Dependencias", len(missing) == 0))

# 3. Verificar estructura de archivos
print("\n3️⃣  Verificando estructura de archivos...")
required_files = [
    'backend/app/main.py',
    'backend/app/parsers/bc3_parser.py',
    'backend/app/generators/pdf_generator.py',
    'backend/app/routes/convert.py',
    'examples/ejemplo_basico.bc3'
]

missing_files = []
for file_path in required_files:
    if os.path.exists(file_path):
        print(f"   ✅ {file_path}")
    else:
        print(f"   ❌ {file_path} (falta)")
        missing_files.append(file_path)

results.append(("Archivos", len(missing_files) == 0))

# 4. Verificar archivo .env
print("\n4️⃣  Verificando configuración...")
env_file = 'backend/.env'
if os.path.exists(env_file):
    print(f"   ✅ {env_file} existe")
    with open(env_file) as f:
        content = f.read()
        if 'ANTHROPIC_API_KEY' in content and 'your_' not in content:
            print("   ✅ ANTHROPIC_API_KEY configurada")
            results.append(("API Key", True))
        else:
            print("   ⚠️  ANTHROPIC_API_KEY no configurada (funciones de IA no disponibles)")
            results.append(("API Key", False))
else:
    print(f"   ⚠️  {env_file} no existe (crea uno desde .env.example)")
    results.append(("Configuración", False))

# 5. Test de parseo BC3
print("\n5️⃣  Probando parser BC3...")
try:
    sys.path.insert(0, 'backend')
    from app.parsers.bc3_parser import BC3Parser

    parser = BC3Parser()
    budget = parser.parse_file('examples/ejemplo_basico.bc3')

    if budget and len(budget.chapters) > 0:
        print(f"   ✅ Parser BC3 funciona")
        print(f"   📊 {len(budget.chapters)} capítulos, Total: {float(budget.total):.2f} EUR")
        results.append(("Parser BC3", True))
    else:
        print("   ❌ Parser BC3 no generó resultado válido")
        results.append(("Parser BC3", False))

except Exception as e:
    print(f"   ❌ Error en parser: {e}")
    results.append(("Parser BC3", False))

# 6. Test de generación PDF
print("\n6️⃣  Probando generador PDF...")
try:
    from app.generators.pdf_generator import PDFGenerator
    import tempfile

    generator = PDFGenerator()
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        tmp_path = tmp.name

    generator.generate_file(budget, tmp_path)

    if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 0:
        print(f"   ✅ Generador PDF funciona ({os.path.getsize(tmp_path)} bytes)")
        os.unlink(tmp_path)
        results.append(("Generador PDF", True))
    else:
        print("   ❌ PDF no generado correctamente")
        results.append(("Generador PDF", False))

except Exception as e:
    print(f"   ❌ Error en generador: {e}")
    results.append(("Generador PDF", False))

# Resumen
print("\n" + "=" * 60)
print(" RESUMEN")
print("=" * 60)

passed = sum(1 for _, status in results if status)
total = len(results)

for name, status in results:
    icon = "✅" if status else "❌"
    print(f"{icon} {name}")

print()
if passed == total:
    print(f"🎉 TODO PERFECTO! ({passed}/{total} checks pasados)")
    print()
    print("🚀 Puedes ejecutar la aplicación con:")
    print("   cd backend && python -m app.main")
    sys.exit(0)
else:
    print(f"⚠️  {passed}/{total} checks pasados")
    print()
    print("🔧 Soluciones:")

    if missing:
        print(f"\n   Instalar dependencias faltantes:")
        print(f"   cd backend && pip install {' '.join(missing)}")

    if not results[dict(results)["Configuración"]]:
        print(f"\n   Crear archivo de configuración:")
        print(f"   cd backend && cp .env.example .env")
        print(f"   Luego edita .env y añade tu ANTHROPIC_API_KEY")

    sys.exit(1)
