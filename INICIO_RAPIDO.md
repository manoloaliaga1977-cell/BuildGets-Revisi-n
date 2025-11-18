# 🚀 INICIO RÁPIDO - Budget Converter

## ⚡ Opción 1: GitHub Codespaces (MÁS FÁCIL)

1. Ve a: https://github.com/manoloaliaga1977-cell/BuildGets-Revisi-n
2. Cambia a la rama: `claude/budget-import-export-app-018MrqiAfdsFifaz42UUDLVR`
3. Clic en **`<> Code`** → **`Codespaces`** → **`Create codespace`**
4. Espera 1-2 minutos
5. En la terminal, ejecuta:

```bash
python3 diagnose.py
```

Si todo está OK ✅, ejecuta:

```bash
cd backend
python3 start.py
```

6. Cuando veas "Uvicorn running...", ve a la pestaña **PORTS** → puerto **8000** → clic en el globo 🌐
7. Añade `/docs` a la URL
8. ¡Prueba la API!

---

## 🌐 Opción 2: Render (100% Gratis, Sin tarjeta)

1. Ve a: **https://render.com/**
2. Regístrate con GitHub
3. **New +** → **Web Service**
4. Conecta tu repositorio: `BuildGets-Revisi-n`
5. Configuración:
   - **Branch:** `claude/budget-import-export-app-018MrqiAfdsFifaz42UUDLVR`
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python start.py`
6. **Environment Variables:**
   - `ANTHROPIC_API_KEY` = tu_clave (opcional)
7. **Plan:** Free
8. **Create Web Service**
9. Espera 3-5 minutos
10. Tu URL: `https://tu-app.onrender.com/docs`

---

## 🧪 VERIFICAR QUE TODO FUNCIONA

### Ejecuta el diagnóstico:

```bash
python3 diagnose.py
```

Debe mostrar TODO en verde ✅

### Prueba manual:

1. Ve a `/docs` en tu navegador
2. Expande `POST /convert/bc3-to-pdf`
3. Clic en **"Try it out"**
4. Sube `examples/ejemplo_basico.bc3`
5. Clic en **"Execute"**
6. Descarga el PDF generado

---

## ❌ SI ALGO FALLA

### Error: "Module not found"

```bash
cd backend
pip install -r requirements.txt
```

### Error: "AI features not available"

No es crítico. BC3→PDF funciona sin IA. Si quieres IA:

1. Ve a: https://console.anthropic.com/
2. Regístrate (gratis, $5 de crédito)
3. Crea API Key
4. Añádela en `.env` o como variable de entorno

### Error: El servidor no inicia

```bash
cd backend
python3 -m app.main
```

O directamente:

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 📊 FUNCIONES DISPONIBLES

### ✅ SIN API KEY (Funciona siempre):
- BC3 → PDF ✅
- BC3 → JSON ✅
- JSON → BC3 ✅
- JSON → PDF ✅

### 🤖 CON API KEY (Requiere Anthropic):
- PDF → BC3 (extracción con IA)
- Mejorar descripciones con IA
- Validar presupuesto con IA

---

## 🎯 URLS IMPORTANTES

- **Docs API:** `tu-url/docs`
- **Health check:** `tu-url/health`
- **Anthropic:** https://console.anthropic.com/
- **GitHub:** https://github.com/manoloaliaga1977-cell/BuildGets-Revisi-n

---

## 💡 TIPS

1. **Primera vez:** Tarda 1-2 minutos instalando dependencias
2. **En Codespaces:** 60 horas gratis/mes
3. **En Render:** Se duerme tras 15 min (tarda 30s en despertar)
4. **Local:** `python3 diagnose.py` antes de empezar

---

**¿Problemas?** Corre `python3 diagnose.py` y mira qué falla ❌
