# Backend - Budget Converter API

Backend de la aplicación Budget Converter construido con FastAPI.

## 🏗️ Arquitectura

### Módulos Principales

#### 1. Models (`app/models/`)

Define los modelos de datos Pydantic para presupuestos:

- `Budget`: Estructura completa del presupuesto
- `BudgetChapter`: Capítulo o subcapítulo
- `BudgetItem`: Partida individual
- `BudgetMetadata`: Información general del presupuesto

#### 2. Parsers (`app/parsers/`)

Parsers para diferentes formatos:

- `BC3Parser`: Lee archivos BC3 (FIEBDC-3)

#### 3. Generators (`app/generators/`)

Generadores de archivos:

- `BC3Generator`: Genera archivos BC3
- `PDFGenerator`: Genera PDFs con ReportLab

#### 4. AI (`app/ai/`)

Servicios de inteligencia artificial:

- `PDFExtractor`: Extrae presupuestos de PDF usando Claude
- `BudgetEnhancer`: Mejora y valida presupuestos

#### 5. Routes (`app/routes/`)

Endpoints de la API:

- `convert.py`: Conversiones entre formatos
- `ai.py`: Funcionalidades de IA

## 🚀 Instalación

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
```

## ⚙️ Configuración

Edita el archivo `.env`:

```bash
API_HOST=0.0.0.0
API_PORT=8000
ANTHROPIC_API_KEY=tu_clave_api_aqui
MAX_FILE_SIZE=10485760
UPLOAD_DIR=uploads
```

## 🏃 Ejecutar

```bash
# Desarrollo
python -m app.main

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 API Documentation

Una vez ejecutado, accede a:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Testing

```bash
# Instalar dependencias de test
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest
```

## 📝 Uso Programático

### Parser BC3

```python
from app.parsers.bc3_parser import BC3Parser

parser = BC3Parser()
budget = parser.parse_file('presupuesto.bc3')

print(f"Total: {budget.total}")
print(f"Partidas: {budget.total_items}")

for chapter in budget.chapters:
    print(f"{chapter.code}: {chapter.title}")
```

### Generar BC3

```python
from app.generators.bc3_generator import BC3Generator
from app.models.budget import Budget, BudgetChapter, BudgetItem
from decimal import Decimal

# Crear presupuesto
budget = Budget()
chapter = BudgetChapter(code="CAP01", title="Capítulo 1")
item = BudgetItem(
    code="PART01",
    description="Partida ejemplo",
    unit="m2",
    price=Decimal("25.50"),
    quantity=Decimal("100")
)
chapter.items.append(item)
budget.chapters.append(chapter)

# Generar BC3
generator = BC3Generator()
generator.generate_file(budget, 'output.bc3')
```

### Generar PDF

```python
from app.generators.pdf_generator import PDFGenerator

generator = PDFGenerator()
generator.generate_file(budget, 'output.pdf')
```

### Extracción con IA

```python
from app.ai.pdf_extractor import PDFExtractor

extractor = PDFExtractor()
budget = extractor.extract_from_file('presupuesto.pdf')
```

### Mejora con IA

```python
from app.ai.budget_enhancer import BudgetEnhancer

enhancer = BudgetEnhancer()
enhanced_budget = enhancer.enhance_descriptions(budget)
validation = enhancer.validate_budget(budget)

print(validation)
```

## 🔒 Seguridad

- Validación de tipos de archivo
- Límite de tamaño de archivos
- CORS configurado
- No se almacenan archivos permanentemente

## 🐛 Debugging

```bash
# Modo debug
uvicorn app.main:app --reload --log-level debug

# Ver logs
tail -f logs/app.log
```

## 📦 Dependencias Principales

- **FastAPI**: Framework web
- **Pydantic**: Validación de datos
- **ReportLab**: Generación de PDF
- **pdfplumber**: Lectura de PDF
- **Anthropic**: Cliente de Claude AI
- **python-multipart**: Upload de archivos

## 🔧 Personalización

### Añadir Nuevo Endpoint

```python
# app/routes/custom.py
from fastapi import APIRouter

router = APIRouter(prefix="/custom", tags=["custom"])

@router.get("/endpoint")
async def custom_endpoint():
    return {"message": "Custom endpoint"}

# app/main.py
from app.routes import custom_router
app.include_router(custom_router)
```

### Añadir Nuevo Campo al Modelo

```python
# app/models/budget.py
class BudgetItem(BaseModel):
    # ... campos existentes ...
    custom_field: Optional[str] = None
```

## 🚀 Despliegue

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
```

## 📊 Performance

- Procesamiento asíncrono
- Archivos temporales limpios automáticamente
- Streaming de archivos grandes
- Rate limiting recomendado para producción
