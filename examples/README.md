# Ejemplos de Uso

Esta carpeta contiene ejemplos y scripts de prueba para Budget Converter.

## Archivos Incluidos

### ejemplo_basico.bc3

Archivo BC3 de ejemplo con:
- 2 capítulos (Demoliciones y Cimentación)
- 6 partidas diferentes
- Precios y cantidades realistas
- Estructura jerárquica completa

### test_api.py

Script de Python para probar todos los endpoints de la API:

```bash
# Asegúrate de que el backend esté corriendo
python test_api.py
```

El script realiza las siguientes pruebas:
1. Health check del servidor
2. Conversión BC3 → JSON
3. Conversión BC3 → PDF
4. Validación con IA
5. Mejora con IA

## Uso de ejemplo_basico.bc3

### Convertir a PDF

```bash
curl -X POST "http://localhost:8000/convert/bc3-to-pdf" \
  -F "file=@ejemplo_basico.bc3" \
  --output ejemplo_basico.pdf
```

### Convertir a JSON

```bash
curl -X POST "http://localhost:8000/convert/bc3-to-json" \
  -F "file=@ejemplo_basico.bc3" \
  -o ejemplo_basico.json
```

### Mejorar con IA

```bash
curl -X POST "http://localhost:8000/ai/enhance-bc3" \
  -F "file=@ejemplo_basico.bc3" \
  -o ejemplo_mejorado.json
```

## Crear tus propios archivos BC3

### Estructura Básica

```
V|FIEBDC-3/2004|~
K|1|Título del Presupuesto|~
K|2|Nombre de la Empresa|~
K|3|DD/MM/YYYY|~
D|##|CAP01\1\\\|~
C|CAP01||Nombre del Capítulo|0,00||0|~
D|CAP01|PART01\100.00\\\|~
C|PART01|m2|Descripción de la partida|25,50||1|~
```

### Campos del Registro C (Concepto)

```
C|código|unidad|descripción|precio||tipo|~
```

- `código`: Identificador único
- `unidad`: ud, m2, m3, ml, kg, etc.
- `descripción`: Texto descriptivo
- `precio`: Precio unitario (usar coma como decimal)
- `tipo`: 0=capítulo, 1=partida

### Campos del Registro D (Descomposición)

```
D|código_padre|código_hijo\cantidad\\\|~
```

- `código_padre`: Código del concepto padre
- `código_hijo`: Código del concepto hijo
- `cantidad`: Cantidad del hijo

## Ejemplos de Python

### Leer un BC3

```python
from backend.app.parsers.bc3_parser import BC3Parser

parser = BC3Parser()
budget = parser.parse_file('ejemplo_basico.bc3')

print(f"Título: {budget.metadata.title}")
print(f"Total: {budget.total} €")

for chapter in budget.chapters:
    print(f"\n{chapter.code}: {chapter.title}")
    for item in chapter.items:
        print(f"  - {item.code}: {item.description}")
        print(f"    {item.quantity} {item.unit} x {item.price}€ = {item.total}€")
```

### Crear un BC3

```python
from backend.app.generators.bc3_generator import BC3Generator
from backend.app.models.budget import Budget, BudgetChapter, BudgetItem, BudgetMetadata
from decimal import Decimal
from datetime import datetime

# Crear presupuesto
metadata = BudgetMetadata(
    title="Mi Presupuesto",
    owner="Mi Empresa S.L.",
    date=datetime.now()
)

budget = Budget(metadata=metadata)

# Crear capítulo
chapter = BudgetChapter(
    code="CAP01",
    title="Trabajos Preliminares"
)

# Añadir partidas
chapter.items.append(BudgetItem(
    code="PART01",
    unit="m2",
    description="Demolición de solera",
    price=Decimal("15.50"),
    quantity=Decimal("50.00")
))

chapter.items.append(BudgetItem(
    code="PART02",
    unit="m3",
    description="Excavación de tierras",
    price=Decimal("25.00"),
    quantity=Decimal("100.00")
))

budget.chapters.append(chapter)

# Generar BC3
generator = BC3Generator()
generator.generate_file(budget, 'mi_presupuesto.bc3')

print(f"Presupuesto generado: {budget.total}€")
```

### Generar PDF

```python
from backend.app.generators.pdf_generator import PDFGenerator

generator = PDFGenerator()
generator.generate_file(budget, 'mi_presupuesto.pdf')
```

## Pruebas Manuales

### 1. Probar el Parser

```bash
cd backend
python -c "
from app.parsers.bc3_parser import BC3Parser
parser = BC3Parser()
budget = parser.parse_file('../examples/ejemplo_basico.bc3')
print(f'Total: {budget.total}€')
print(f'Capítulos: {len(budget.chapters)}')
"
```

### 2. Generar PDF de Ejemplo

```bash
cd backend
python -c "
from app.parsers.bc3_parser import BC3Parser
from app.generators.pdf_generator import PDFGenerator

parser = BC3Parser()
budget = parser.parse_file('../examples/ejemplo_basico.bc3')

generator = PDFGenerator()
generator.generate_file(budget, '../examples/ejemplo_output.pdf')
print('PDF generado: ejemplo_output.pdf')
"
```

### 3. Probar IA (requiere API key)

```bash
cd backend
python -c "
from app.parsers.bc3_parser import BC3Parser
from app.ai.budget_enhancer import BudgetEnhancer

parser = BC3Parser()
budget = parser.parse_file('../examples/ejemplo_basico.bc3')

enhancer = BudgetEnhancer()
validation = enhancer.validate_budget(budget)

print('Validación:', validation)
"
```

## Notas

- Los archivos BC3 usan codificación `latin-1` (ISO-8859-1)
- Los decimales en BC3 usan coma (,) en lugar de punto (.)
- Los registros terminan con `~`
- Los campos se separan con `|`
- Los subcampos se separan con `\`

## Recursos Adicionales

- [Especificación FIEBDC-3](http://www.fiebdc.org/)
- [Ejemplos de BC3 reales](http://www.preoc.es/)
- Documentación de la API: http://localhost:8000/docs
