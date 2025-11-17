# 🚀 Guía Rápida para Replit

## Paso 1: Importar el Proyecto

1. Ve a https://replit.com/
2. Clic en **"+ Create Repl"**
3. Selecciona **"Import from GitHub"**
4. Pega esta URL:
   ```
   https://github.com/manoloaliaga1977-cell/BuildGets-Revisi-n
   ```
5. Rama: `claude/budget-import-export-app-018MrqiAfdsFifaz42UUDLVR`
6. Clic en **"Import from GitHub"**

## Paso 2: Configurar API Key

1. En Replit, haz clic en el icono de **candado** 🔒 (Secrets)
2. Clic en **"New secret"**
3. **Key:** `ANTHROPIC_API_KEY`
4. **Value:** tu clave de Anthropic (obtén una gratis en https://console.anthropic.com/)
5. Clic en **"Add secret"**

## Paso 3: Ejecutar

1. Haz clic en el botón verde **"Run"** ▶️
2. Espera 1-2 minutos mientras instala las dependencias
3. Replit abrirá automáticamente la aplicación en un navegador integrado

## Paso 4: Usar la Aplicación

1. Sube un archivo BC3 (puedes usar `examples/ejemplo_basico.bc3`)
2. Selecciona el tipo de conversión (ej: BC3 → PDF)
3. Haz clic en **"Convertir"**
4. Descarga el archivo convertido

## 📍 URLs

Cuando esté ejecutándose, tu app estará disponible en:
- URL de Replit: `https://[tu-proyecto].repl.co`
- Backend API: Mismo URL + `/docs` para ver la documentación

## ⚠️ Problemas Comunes

### "Module not found" o errores de dependencias
- **Solución**: Espera a que termine la instalación (mira la consola)
- Si persiste, ve a la pestaña "Shell" y ejecuta:
  ```bash
  cd backend
  pip install -r requirements.txt
  ```

### "AI features not available"
- **Solución**: Verifica que añadiste `ANTHROPIC_API_KEY` en Secrets (candado 🔒)

### "Connection error" o "Network error"
- **Solución**:
  1. Abre la consola del navegador (F12)
  2. Busca errores de CORS o conexión
  3. Verifica que el backend esté corriendo (debe decir "Running on http://0.0.0.0:8000")

### Los archivos no se procesan
- **Solución**:
  1. Abre la consola del navegador (F12)
  2. Verifica que la URL de la API sea correcta (debe mostrar algo como "API URL configurada: https://...")
  3. Verifica que el archivo sea del tipo correcto (.bc3 o .pdf)

### "500 Internal Server Error"
- **Solución**:
  1. Revisa los logs en la consola de Replit
  2. El error más común es que falta la API key de Anthropic
  3. O que el archivo BC3 tiene un formato incorrecto

## 📦 Archivos de Ejemplo

El proyecto incluye un archivo de ejemplo listo para probar:
- `examples/ejemplo_basico.bc3` - Presupuesto de construcción de ejemplo

Úsalo para probar que todo funciona antes de subir tus propios archivos.

## 🔧 Configuración Avanzada

### Cambiar Puerto
Si necesitas cambiar el puerto, edita `backend/.env`:
```
API_PORT=8000
```

### Desactivar IA (solo procesamiento básico)
Si no tienes API key de Anthropic, la app funcionará pero sin funciones de IA:
- ✅ BC3 → PDF (funciona)
- ✅ BC3 → JSON (funciona)
- ❌ PDF → BC3 (requiere IA)
- ❌ Mejorar con IA (requiere IA)

## 💡 Consejos

1. **Primera ejecución**: Tarda ~2 minutos en instalar dependencias
2. **Ejecuciones siguientes**: Tarda ~10 segundos en arrancar
3. **Inactividad**: Replit apaga la app después de 1 hora sin uso
4. **Rearranque**: Solo haz clic en "Run" de nuevo

## 🆘 Ayuda

Si algo no funciona:
1. Verifica los logs en la consola de Replit
2. Abre la consola del navegador (F12) y busca errores
3. Revisa que tu archivo BC3/PDF sea válido
4. Abre un issue en GitHub con los detalles del error

---

**¡Listo para probar!** 🎉
