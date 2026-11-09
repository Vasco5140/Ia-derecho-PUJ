# 🚀 Hito M4 — Guía de Despliegue con URL Pública

**Proyecto:** Sis AI — Asesoría legal sobre vivienda y sismos  
**Estudiante:** Jose David Vasco  
**Materia:** Derecho e Inteligencia Artificial · Pontificia Universidad Javeriana  
**Docente:** Pedro Ardila  

---

## 🎯 Objetivo de este Hito

Llevar la aplicación web **Sis AI** desde tu computador a una **URL pública en internet** accesible para cualquier persona, evaluador o usuario real desde su celular o computador, sin pagar servidores y sin requerir tarjeta de crédito.

---

## ☁️ Plataforma Seleccionada: Streamlit Community Cloud (100% Gratuita)

El curso recomienda en la **Parte 3 y 4 del README** el uso de **Streamlit** para agentes en Python desplegados en la nube ([`streamlit.io/community-cloud`](https://streamlit.io)).

### ¿Por qué esta opción?
1. **Conexión directa con GitHub:** Cada vez que actualizas un archivo en tu repositorio, la web se actualiza sola en segundos.
2. **Cero configuración de servidores:** No tienes que configurar Linux ni Docker.
3. **URL pública permanente:** Te entrega un enlace oficial tipo `https://tu-proyecto.streamlit.app`.

---

## 📋 Paso a Paso para Desplegar (En 3 Minutos)

### Paso 1: Asegurarte de que tus archivos estén en GitHub
Antes de desplegar, los siguientes archivos deben estar subidos en tu repositorio [https://github.com/Vasco5140/Ia-derecho-PUJ](https://github.com/Vasco5140/Ia-derecho-PUJ):
- `app.py`
- `requirements.txt`
- `.streamlit/config.toml`
- Carpeta `corpus/` con las normas

---

### Paso 2: Crear tu cuenta en Streamlit Cloud
1. Entra a 👉 [https://share.streamlit.io](https://share.streamlit.io)
2. Haz clic en **"Continue with GitHub"** (Inicia sesión con la misma cuenta de GitHub donde tienes el proyecto).
3. Autoriza la conexión de Streamlit con tu cuenta de GitHub.

---

### Paso 3: Crear la Aplicación ("Create App")
1. En tu panel de Streamlit Cloud, haz clic en el botón azul superior: **`Create app`** (o `New app`).
2. Selecciona la opción **"I already have an app"** (o "Deploy a public app from GitHub").
3. Completa los 3 campos:
   * **Repository:** Escribe o selecciona `Vasco5140/Ia-derecho-PUJ`
   * **Branch:** `main`
   * **Main file path:** `app.py`
   * *(Opcional)* **App URL:** Puedes personalizar la dirección (ej. `sis-ai-javeriana.streamlit.app`).

---

### Paso 4: Configurar la clave de IA (Opcional - Secrets)
Si tienes una clave de **OpenRouter**:
1. En la misma pantalla de despliegue, haz clic en **"Advanced settings"**.
2. En el recuadro **Secrets**, pega:
   ```toml
   OPENROUTER_API_KEY = "tu_clave_aqui"
   ```
3. *(Si no tienes clave todavía, no te preocupes: Sis AI tiene un motor RAG local integrado que funciona automáticamente sin API key).*

---

### Paso 5: ¡Hacer clic en Deploy! 🚀
1. Haz clic en el botón azul **`Deploy!`**.
2. Verás una animación mientras Streamlit instala las librerías (`requirements.txt`) y enciende la web.
3. ¡Listo! Tu aplicación estará al aire con una URL pública funcional.

---

## ✅ Checklist de Validación del Hito M4

- [x] **Aplicación interactiva desarrollada:** Interfaz de chat, generador formal de minutas y visor del corpus normativo (`app.py`).
- [x] **Salvaguarda ética visible:** Advertencia obligatoria mostrada de forma prominente en la cabecera de la página y en las respuestas.
- [x] **Protección de datos (Ley 1581 de 2012):** La interfaz avisa al usuario no ingresar datos sensibles y anonimiza con corchetes `[Nombre del Asegurado]`.
- [ ] **URL pública anotada:** Copia el enlace generado en la Parte 4 del `README.md`.
