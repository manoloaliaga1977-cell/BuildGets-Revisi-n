# Budget Converter - Desplegado en la Nube ☁️

¿No puedes o no quieres instalar nada localmente? **¡No problem!** Puedes ejecutar toda la aplicación en la nube de forma gratuita.

## 🚀 Guía Visual Completa

Abre este archivo en tu navegador para una guía paso a paso:

👉 **[DESPLEGAR_ONLINE.html](./DESPLEGAR_ONLINE.html)**

## ⚡ Opciones Rápidas

### Opción 1: Railway (Recomendado)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template)

1. Haz clic en el botón de arriba
2. Conecta tu cuenta de GitHub
3. Selecciona este repositorio
4. Añade tu `ANTHROPIC_API_KEY`
5. ¡Listo! Tu app estará en: `https://tu-app.up.railway.app`

**Ventajas:**
- ✅ $5 gratis al mes (suficiente para empezar)
- ✅ Despliegue automático desde GitHub
- ✅ Backend + Frontend juntos
- ✅ Muy rápido y fácil

**Requisitos:**
- Cuenta de GitHub
- Tarjeta de crédito (no cobra en plan gratuito)

---

### Opción 2: Render (100% Gratis)

1. Ve a [render.com](https://render.com/)
2. Regístrate con GitHub
3. Crea un "Web Service"
4. Conecta este repositorio
5. Configura:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Añade variable de entorno: `ANTHROPIC_API_KEY`

**Ventajas:**
- ✅ 100% gratis sin tarjeta de crédito
- ✅ SSL automático
- ✅ Despliegue desde GitHub

**Limitaciones:**
- ⚠️ Se duerme después de 15 min de inactividad
- ⚠️ Arranque lento (30-60 segundos)

---

### Opción 3: Replit (Para Desarrollo)

1. Ve a [replit.com](https://replit.com/)
2. Crea cuenta gratuita
3. "Import from GitHub"
4. Pega la URL de este repo
5. Añade `ANTHROPIC_API_KEY` en Secrets
6. Haz clic en "Run"

**Ventajas:**
- ✅ Sin instalación
- ✅ Editor de código en el navegador
- ✅ Gratis sin tarjeta

**Limitaciones:**
- ⚠️ Se apaga cuando cierras el navegador
- ⚠️ No recomendado para producción

---

## 🔑 Obtener API Key de Anthropic

Todas las opciones requieren una API key de Anthropic:

1. Ve a: https://console.anthropic.com/
2. Regístrate o inicia sesión
3. Ve a "API Keys"
4. Crea una nueva key
5. Cópiala (empieza con `sk-ant-...`)

**Precio:** $5 de crédito gratis, luego ~$0.003 por conversión

---

## 📊 Comparación Rápida

| Característica | Railway | Render | Replit |
|---------------|---------|--------|--------|
| **Precio** | $5 gratis/mes | 100% gratis | Gratis |
| **Tarjeta requerida** | Sí (no cobra) | No | No |
| **Siempre activo** | ✅ | ❌ | ❌ |
| **Velocidad** | Rápido | Lento (30-60s) | Medio |
| **Para producción** | ✅ | ✅ | ❌ |
| **Dificultad** | Fácil | Media | Muy fácil |

---

## 🎯 Recomendación

- **¿Tienes tarjeta de crédito?** → **Railway** (mejor opción)
- **¿Sin tarjeta?** → **Render** (100% gratis)
- **¿Solo quieres probar?** → **Replit** (más rápido de configurar)

---

## 📝 Archivos de Configuración Incluidos

Este repositorio ya incluye los archivos necesarios para desplegar en estas plataformas:

```
backend/
├── Procfile          # Para Railway/Render
├── runtime.txt       # Versión de Python
└── railway.json      # Configuración Railway
```

**¡No necesitas modificar nada!** Solo conéctalo y añade tu API key.

---

## 🌐 URLs de Ejemplo

Después del despliegue, tu app estará disponible en:

- **Railway**: `https://tu-app.up.railway.app`
- **Render**: `https://tu-app.onrender.com`
- **Replit**: `https://tu-app.your-username.repl.co`

---

## ❓ ¿Necesitas Ayuda?

- 📖 Lee la [guía visual completa](./DESPLEGAR_ONLINE.html)
- 💬 Abre un [issue en GitHub](https://github.com/manoloaliaga1977-cell/BuildGets-Revisi-n/issues)
- 📚 Consulta el [README principal](./README.md)

---

**¡Tu aplicación funcionando en internet sin instalar nada!** 🎉
