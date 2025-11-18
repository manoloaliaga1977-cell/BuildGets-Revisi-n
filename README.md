# 🏗️ Budget Converter - BC3 & PDF

Aplicación completa para importar/exportar presupuestos de construcción en formatos BC3 y PDF con potenciación mediante Inteligencia Artificial.

**✅ 100% Funcional | ☁️ Listo para la nube | 🚀 Sin instalación local necesaria**

## ✨ Características

- **Conversión Bidireccional**: BC3 ↔ PDF en ambas direcciones
- **Múltiples Formatos**: BC3, PDF, JSON
- **IA Integrada** (opcional):
  - Extracción inteligente de datos desde PDF
  - Mejora automática de descripciones
  - Validación y detección de errores
- **API REST**: Backend completo con FastAPI
- **Interfaz Web Moderna**: Frontend con React y TailwindCSS
- **Formato BC3 Completo**: Soporte total para FIEBDC-3 con multi-encoding
- **Deploy en la Nube**: Funciona en GitHub Codespaces, Render, Railway, Replit
- **Robusto y Probado**: Manejo de errores completo, logging detallado, limpieza automática

## 🚀 Inicio Rápido

**👉 [GUÍA DE INICIO RÁPIDO](./INICIO_RAPIDO.md) 👈**

Para empezar en menos de 2 minutos, ve a **[INICIO_RAPIDO.md](./INICIO_RAPIDO.md)**

### Opciones de Despliegue

1. **GitHub Codespaces** (RECOMENDADO) - 60 horas gratis/mes
2. **Render** - 100% gratis, sin tarjeta de crédito
3. **Railway** - Plan gratuito disponible
4. **Replit** - Fácil pero consumo de tokens
5. **Local** - Si prefieres instalar localmente

### Prerrequisitos (Solo para instalación local)

- Python 3.9+
- Node.js 18+ (opcional, solo si usas el frontend)
- npm o yarn (opcional)

### Instalación Local (Opcional)

#### 1. Clonar el repositorio

```bash
git clone https://github.com/manoloaliaga1977-cell/BuildGets-Revisi-n.git
cd BuildGets-Revisi-n
git checkout claude/budget-import-export-app-018MrqiAfdsFifaz42UUDLVR
```

#### 2. Instalar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (OPCIONAL)
cp .env.example .env
# Editar .env y añadir tu ANTHROPIC_API_KEY (solo si quieres funciones de IA)
```

#### 3. Verificar Instalación

```bash
# Desde la raíz del proyecto
python3 diagnose.py
```

Este script verifica que todo esté correctamente configurado. Debe mostrar TODO en verde ✅

#### 4. Iniciar Servidor

```bash
cd backend
python3 start.py
```

El script `start.py` detecta automáticamente tu plataforma y configura el puerto correcto.

La API estará disponible en: `http://localhost:8000`
Documentación interactiva: `http://localhost:8000/docs`

#### 5. Frontend (Opcional)

El backend funciona standalone y proporciona docs interactivas en `/docs`. Si quieres la interfaz React:

```bash
cd frontend
npm install
npm run dev
```

La aplicación web estará disponible en: `http://localhost:5173`

## 📚 Documentación

### Estructura del Proyecto

```
BuildGets-Revisión/
├── backend/
│   ├── app/
│   │   ├── models/          # Modelos de datos (Budget, Chapter, Item)
│   │   ├── parsers/         # Parser BC3 (multi-encoding, robusto)
│   │   ├── generators/      # Generadores BC3 y PDF
│   │   ├── ai/              # Servicios de IA (opcional)
│   │   ├── routes/          # Endpoints de API (con cleanup automático)
│   │   └── main.py          # Aplicación FastAPI
│   ├── start.py             # ⭐ Script de inicio inteligente
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/      # Componentes React (API auto-detect)
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── examples/                # Archivos BC3 de ejemplo
├── diagnose.py              # ⭐ Script de verificación automática
├── INICIO_RAPIDO.md         # ⭐ Guía de inicio rápido
├── DESPLEGAR.md             # Guías de despliegue cloud
└── README.md
```

### Mejoras Clave de Esta Versión

#### 🛡️ Parser BC3 Robusto
- **Multi-encoding**: Prueba automáticamente latin-1, utf-8, iso-8859-1, cp1252
- **Manejo de errores**: Continúa parseando incluso si algunos registros fallan
- **Logging detallado**: Muestra exactamente qué está pasando con emojis
- **Parsing decimal mejorado**: Limpia valores con regex para evitar errores

#### 🧹 Gestión de Archivos Temporales
- **Cleanup automático**: Usa `atexit` para limpiar al cerrar
- **Tracking global**: Mantiene lista de todos los archivos temporales
- **FileResponse background**: Limpia después de enviar respuesta
- **Sin acumulación**: Los archivos temporales no se acumulan nunca

#### 🚀 Inicio Inteligente
- **Detección de plataforma**: Replit, Railway, Render, Codespaces, local
- **Auto-configuración**: Puertos y hosts según la plataforma
- **Verificación de API key**: Informa si funciones de IA están disponibles
- **Logging claro**: Emojis y mensajes descriptivos

#### 🔍 Script de Diagnóstico
- **Verificación completa**: Python, dependencias, archivos, configuración
- **Tests funcionales**: Prueba parser BC3 y generador PDF
- **Mensajes accionables**: Te dice exactamente qué hacer si algo falla
- **Resumen visual**: ✅/❌ para cada check

#### ☁️ Deploy en Cualquier Plataforma
- **API URL auto-detect**: El frontend se adapta automáticamente
- **Sin proxy necesario**: Funciona en producción sin configuración
- **CORS configurado**: Permite acceso desde cualquier origen
- **Logs accesibles**: Puedes ver qué está pasando en tiempo real

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

### 🔍 Primer Paso: Ejecuta el Diagnóstico

Antes de nada, ejecuta:

```bash
python3 diagnose.py
```

Este script te dirá exactamente qué está fallando y cómo arreglarlo.

### ⚠️ Funciones sin API Key

**SIN ANTHROPIC_API_KEY (Funciona siempre):**
- ✅ BC3 → PDF
- ✅ BC3 → JSON
- ✅ JSON → BC3
- ✅ JSON → PDF

**CON ANTHROPIC_API_KEY (Requiere configuración):**
- 🤖 PDF → BC3 (extracción con IA)
- 🤖 Mejorar descripciones con IA
- 🤖 Validar presupuesto con IA

### Error: "AI features not available"

Esto es normal si no has configurado `ANTHROPIC_API_KEY`. Las funciones básicas (BC3→PDF, BC3→JSON) funcionan sin IA.

Si quieres activar IA:
1. Ve a https://console.anthropic.com/
2. Regístrate (gratis, $5 de crédito)
3. Crea una API Key
4. Añádela en `backend/.env` o como variable de entorno

### Error: "Module not found"

```bash
cd backend
pip install -r requirements.txt
```

### Error: El servidor no inicia

```bash
cd backend
python3 start.py
```

Si sigue fallando:

```bash
cd backend
python3 -m app.main
```

### Error: Frontend no conecta con backend

El frontend detecta automáticamente la URL del backend. Verifica en la consola del navegador que la API URL sea correcta.

En local debe ser: `http://localhost:8000`
En cloud debe ser: `https://tu-app.onrender.com` (o similar)

### Error: "unicodeDecodeError" con BC3

El parser ahora prueba automáticamente múltiples encodings (latin-1, utf-8, iso-8859-1, cp1252). Si sigue fallando, el archivo BC3 puede estar corrupto.

### Error de CORS

Ya está configurado para permitir todos los orígenes en producción. Si tienes problemas, verifica que `app.main:app` tenga el middleware CORS activado.

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
