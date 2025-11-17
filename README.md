# 🏗️ Budget Converter - BC3 & PDF

Aplicación completa para importar/exportar presupuestos de construcción en formatos BC3 y PDF con potenciación mediante Inteligencia Artificial.

## ✨ Características

- **Conversión Bidireccional**: BC3 ↔ PDF en ambas direcciones
- **Múltiples Formatos**: BC3, PDF, JSON
- **IA Integrada**:
  - Extracción inteligente de datos desde PDF
  - Mejora automática de descripciones
  - Validación y detección de errores
- **API REST**: Backend completo con FastAPI
- **Interfaz Web Moderna**: Frontend con React y TailwindCSS
- **Formato BC3 Completo**: Soporte total para FIEBDC-3

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.9+
- Node.js 18+
- npm o yarn

### Instalación

#### 1. Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env y añadir tu ANTHROPIC_API_KEY
```

#### 2. Frontend

```bash
cd frontend

# Instalar dependencias
npm install
```

### Ejecución

#### Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate
python -m app.main

# O usando uvicorn directamente
uvicorn app.main:app --reload --port 8000
```

La API estará disponible en: `http://localhost:8000`
Documentación interactiva: `http://localhost:8000/docs`

#### Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

La aplicación web estará disponible en: `http://localhost:3000`

## 📚 Documentación

### Estructura del Proyecto

```
BuildGets-Revisión/
├── backend/
│   ├── app/
│   │   ├── models/          # Modelos de datos (Budget, Chapter, Item)
│   │   ├── parsers/         # Parser BC3
│   │   ├── generators/      # Generadores BC3 y PDF
│   │   ├── ai/              # Servicios de IA
│   │   ├── routes/          # Endpoints de API
│   │   └── main.py          # Aplicación FastAPI
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── examples/               # Archivos de ejemplo
└── README.md
```

### API Endpoints

#### Conversión

- `POST /convert/bc3-to-pdf` - Convierte BC3 a PDF
  - Query param: `enhance=true` (opcional) - Mejora con IA
- `POST /convert/pdf-to-bc3` - Convierte PDF a BC3
- `POST /convert/bc3-to-json` - Convierte BC3 a JSON
- `POST /convert/pdf-to-json` - Convierte PDF a JSON
- `POST /convert/json-to-bc3` - Convierte JSON a BC3
- `POST /convert/json-to-pdf` - Convierte JSON a PDF

#### IA

- `POST /ai/enhance-budget` - Mejora descripciones con IA
- `POST /ai/validate-budget` - Valida presupuesto
- `POST /ai/enhance-bc3` - Mejora archivo BC3

#### Utilidades

- `GET /` - Información de la API
- `GET /health` - Estado del servicio

### Ejemplos de Uso

#### Usando cURL

```bash
# Convertir BC3 a PDF
curl -X POST "http://localhost:8000/convert/bc3-to-pdf" \
  -F "file=@presupuesto.bc3" \
  --output presupuesto.pdf

# Convertir PDF a BC3 con IA
curl -X POST "http://localhost:8000/convert/pdf-to-bc3" \
  -F "file=@presupuesto.pdf" \
  --output presupuesto.bc3

# Validar presupuesto
curl -X POST "http://localhost:8000/ai/validate-budget" \
  -H "Content-Type: application/json" \
  -d @presupuesto.json
```

#### Usando Python

```python
import requests

# Convertir BC3 a PDF
with open('presupuesto.bc3', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/convert/bc3-to-pdf',
        files=files
    )

    with open('presupuesto.pdf', 'wb') as out:
        out.write(response.content)

# Mejorar con IA
with open('presupuesto.bc3', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/ai/enhance-bc3',
        files=files
    )

    enhanced_budget = response.json()
    print(enhanced_budget)
```

#### Usando JavaScript

```javascript
// Convertir BC3 a PDF
const formData = new FormData();
formData.append('file', bc3File);

const response = await fetch('http://localhost:8000/convert/bc3-to-pdf', {
  method: 'POST',
  body: formData
});

const blob = await response.blob();
const url = window.URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'presupuesto.pdf';
a.click();
```

## 🧠 Funciones de IA

### Extracción desde PDF

La aplicación utiliza Claude AI para extraer información estructurada de PDFs:

- Reconocimiento de capítulos y partidas
- Extracción de códigos, descripciones, cantidades y precios
- Detección automática de unidades de medida
- Estructuración jerárquica del presupuesto

### Mejora de Descripciones

Mejora automática de descripciones técnicas:

- Clarificación de términos técnicos
- Estandarización de formato
- Mejora de legibilidad
- Mantiene información esencial

### Validación Inteligente

Análisis completo del presupuesto:

- Detección de precios sospechosos
- Identificación de partidas duplicadas
- Validación de unidades
- Sugerencias de mejora

## 🔧 Configuración Avanzada

### Variables de Entorno

```bash
# Backend (.env)
API_HOST=0.0.0.0
API_PORT=8000

# Clave de IA (obligatoria para funciones de IA)
ANTHROPIC_API_KEY=tu_clave_aqui

# Configuración adicional
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIR=uploads
```

### Personalización

#### Modificar Estilo PDF

Edita `backend/app/generators/pdf_generator.py`:

```python
# Cambiar colores, fuentes, tamaños, etc.
self.styles.add(ParagraphStyle(
    name='CustomTitle',
    fontSize=18,
    textColor=colors.HexColor('#1a365d'),
    # ...
))
```

#### Añadir Nuevos Campos BC3

Edita `backend/app/models/budget.py` para añadir campos personalizados.

## 📝 Formato BC3

El formato BC3 (FIEBDC-3) es el estándar español para intercambio de presupuestos de construcción.

### Estructura Básica

```
V|FIEBDC-3/2004|~
K|1|Título del Presupuesto|~
C|CAP01|ud|Capítulo 1|0,00||0|~
D|CAP01|PART01\1.00\\|~
C|PART01|m2|Partida ejemplo|25,50||1|~
```

### Tipos de Registros

- `V`: Versión del formato
- `K`: Información general
- `C`: Conceptos (capítulos y partidas)
- `D`: Descomposición (relaciones padre-hijo)

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# API tests
cd examples
python test_api.py
```

## 🐛 Solución de Problemas

### Error: "AI features not available"

Asegúrate de configurar `ANTHROPIC_API_KEY` en el archivo `.env`.

### Error: "Module not found"

Reinstala las dependencias:

```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

### Error de CORS

Verifica que el frontend use el proxy correcto en `vite.config.js`.

## 🤝 Contribuir

Las contribuciones son bienvenidas:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🙏 Agradecimientos

- **FIEBDC** por el estándar BC3
- **Anthropic** por Claude AI
- **FastAPI** y **React** por los frameworks

## 📞 Soporte

Si encuentras algún problema o tienes preguntas:

- Abre un issue en GitHub
- Consulta la documentación en `/docs`
- Revisa los ejemplos en `/examples`

## 🗺️ Roadmap

- [ ] Soporte para BC3 versión 2012
- [ ] Exportación a Excel
- [ ] Importación desde otros formatos (ODBC, Presto, etc.)
- [ ] Editor visual de presupuestos
- [ ] API de comparación de presupuestos
- [ ] Generación de informes personalizados
- [ ] App móvil

---

**Hecho con ❤️ para la industria de la construcción**
