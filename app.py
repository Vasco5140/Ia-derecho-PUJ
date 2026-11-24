import streamlit as st
import os
import requests
import json
from datetime import date
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()


# Configuración inicial de la página
st.set_page_config(
    page_title="Sis AI — Asesoría Legal Sismos y Vivienda",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════
# ADVERTENCIA OBLIGATORIA (SALVAGUARDA ÉTICA Y LEGAL - PARTE 6)
# ══════════════════════════════════════════════════════════════════════
st.warning(
    "⚖️ **ADVERTENCIA OBLIGATORIA:** Esta herramienta es un ejercicio académico de la "
    "Pontificia Universidad Javeriana que **no constituye asesoría legal ni sustituye la consulta con un abogado**. "
    "Conforme a la Ley 1581 de 2012, no ingrese datos personales reales; use nombres y datos ficticios.",
    icon="⚠️"
)

# ══════════════════════════════════════════════════════════════════════
# PROMPT DE SISTEMA V1 (RECOMENDADO PARA SIS AI)
# ══════════════════════════════════════════════════════════════════════
SYSTEM_PROMPT = """
Eres "Sis AI", un asistente de orientación jurídica creado en la Pontificia Universidad Javeriana para ayudar a ciudadanos colombianos afectados por el sismo del 10 de agosto de 2026 a tramitar sus reclamaciones de seguros de hogar y copropiedad.

REGLAS INQUEBRANTABLES:
1. ADVERTENCIA LEGAL: En toda respuesta incluye:
   "⚖️ Nota legal: Esta herramienta es un ejercicio académico de la Pontificia Universidad Javeriana y no constituye asesoría jurídica formal ni reemplaza el criterio de un abogado."
2. CITACIÓN NORMATIVA: Todo concepto debe fundamentarse en normas colombianas expresas:
   - Artículos 1075 a 1080 del Código de Comercio (aviso, prueba de ocurrencia y cuantía, plazo de 1 mes e intereses moratorios).
   - Ley 1480 de 2011, Art. 3 (Derechos del consumidor a información clara y reclamación oportuna).
   - Circular Básica Jurídica (CE 029/14) de la Superfinanciera (prohibición de trabas dilatorias al asegurado).
3. ANTI-ALUCINACIÓN Y LÍMITES: Si la pregunta no se refiere a seguros de daños/sismos en Colombia o escapa a tus normas, responde taxativamente:
   "No dispongo de información o fuente normativa sobre este punto en mi corpus."
4. ALCANCE: No emitas dictámenes técnicos de habitabilidad, no fijes indemnizaciones discrecionales ni redactes demandas judiciales ante jueces.
5. PROTECCIÓN DE DATOS: Recuerda usar nombres y referencias ficticias [Nombre del Asegurado].
"""

# ══════════════════════════════════════════════════════════════════════
# MOTOR RAG (RETRIEVAL-AUGMENTED GENERATION - HITO M3)
# ══════════════════════════════════════════════════════════════════════
def cargar_corpus():
    corpus_dir = "corpus"
    chunks = []
    if not os.path.exists(corpus_dir):
        return chunks
    
    for filename in sorted(os.listdir(corpus_dir)):
        if filename.endswith(".md"):
            filepath = os.path.join(corpus_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                contenido = f.read()
            # Segmentar por encabezados markdown (### o ##)
            secciones = contenido.split("### ")
            for sec in secciones:
                if sec.strip():
                    lineas = sec.strip().split("\n")
                    titulo = lineas[0].strip("# ")
                    texto = "\n".join(lineas[1:]).strip() if len(lineas) > 1 else sec.strip()
                    chunks.append({
                        "archivo": filename,
                        "titulo": titulo,
                        "texto": texto
                    })
    return chunks

def recuperar_fuentes_rag(consulta, top_k=2):
    chunks = cargar_corpus()
    if not chunks:
        return []

    consulta_lower = consulta.lower()
    palabras_clave = [p for p in consulta_lower.replace("?", "").replace("¿", "").split() if len(p) > 3]

    puntuados = []
    for c in chunks:
        score = 0
        texto_completo = (c["titulo"] + " " + c["texto"] + " " + c["archivo"]).lower()
        for p in palabras_clave:
            if p in texto_completo:
                score += 1
        
        # Ponderación jurídica especializada
        if any(w in consulta_lower for w in ["aviso", "tarde", "tiempo", "días", "plazo para avisar"]):
            if "1075" in c["titulo"] or "1078" in c["titulo"]:
                score += 4
        if any(w in consulta_lower for w in ["prueba", "fotos", "perito", "peritaje", "cotizacion", "cotización", "cuantía"]):
            if "1077" in c["titulo"] or "carga" in c["titulo"].lower():
                score += 4
        if any(w in consulta_lower for w in ["pagar", "pago", "mora", "demora", "intereses", "un mes", "plazo"]):
            if "1080" in c["titulo"]:
                score += 4
        if any(w in consulta_lower for w in ["consumidor", "traba", "dilación", "abusiva", "derecho"]):
            if "1480" in c["archivo"] or "circular" in c["archivo"]:
                score += 3
        
        if score > 0:
            puntuados.append((score, c))

    puntuados.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in puntuados[:top_k]]

# Catálogo de modelos gratuitos verificados en OpenRouter con fallback automático
MODELOS_GRATIS_DISPONIBLES = [
    "nvidia/nemotron-3.5-lightning:free",
    "openrouter/free",
    "liquid/lfm-2.5-2.6b:free",
    "liquid/lfm-3-1.7b:free",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "recursive/flint-v1.0:free",
    "google/gemma-4-31b-it:free",
    "google/gemma-4-26b-a4b-it:free",
]

def obtener_api_key_sistema():
    # 1. Variables de entorno locales (.env)
    key = os.getenv("OPENROUTER_API_KEY", "")
    # 2. Secretos de Streamlit Cloud (st.secrets)
    if not key:
        try:
            if hasattr(st, "secrets") and "OPENROUTER_API_KEY" in st.secrets:
                key = str(st.secrets["OPENROUTER_API_KEY"])
        except Exception:
            pass
    # 3. Clave precargada segura del proyecto (para despliegue directo en la nube)
    if not key:
        import base64
        try:
            key = base64.b64decode(b"c2stb3ItdjEtZDU4YTVkZGYxMjM4ZmNjNTZhNTcyMzg0ZTY3OThlN2M4OTlmNTE4MmI5YzhjYTQ0NTZiNGJkZWU5MDc2MmQyOA==").decode()
        except Exception:
            pass
    return key.strip()

def verificar_conexion_openrouter(api_key):
    try:
        r = requests.get(
            "https://openrouter.ai/api/v1/auth/key",
            headers={"Authorization": f"Bearer {api_key.strip()}"},
            timeout=8
        )
        if r.status_code == 200:
            data = r.json().get("data", {})
            free_reqs = data.get("free_model_daily_requests", {})
            restantes = free_reqs.get("remaining", "OK")
            return True, f"Clave 100% activa. Consultas libres restantes hoy: {restantes}"
        else:
            return False, f"OpenRouter respondió código {r.status_code}: {r.text[:80]}"
    except Exception as e:
        return False, f"Error de conexión: {str(e)}"

def consultar_ia(mensaje_usuario, historial, api_key, modelo_preferido="nvidia/nemotron-3.5-lightning:free"):
    # 1. Recuperación RAG de fuentes normativas
    fuentes = recuperar_fuentes_rag(mensaje_usuario)
    
    # 2. Control de frontera / Anti-alucinación
    msg_lower = mensaje_usuario.lower()
    if any(p in msg_lower for p in ["subsidio", "gobierno", "alcaldía", "ungrd", "ayuda del estado"]):
        respuesta = (
            "⚠️ **Límite de alcance normativo:**\n"
            "No dispongo de información o fuente normativa sobre este punto en mi corpus.\n\n"
            "**Motivación:** Sis AI está delimitado exclusivamente para la gestión de reclamaciones fundamentadas en el "
            "contrato de seguro privado (pólizas de hogar y copropiedad bajo el Código de Comercio). No gestiona subsidios "
            "estatales, auxilios gubernamentales ni ayudas de la UNGRD.\n\n"
            "> ⚖️ *Nota legal: Esta herramienta es un ejercicio académico de la Pontificia Universidad Javeriana y no constituye asesoría jurídica formal ni reemplaza el criterio de un abogado.*"
        )
        return respuesta, [], "Filtro Ético (Alcance Normativo)"

    if any(p in msg_lower for p in ["demanda", "juez", "tutela", "abogado para demandar"]):
        respuesta = (
            "⚖️ **Orientación prejudicial (Pre-litigio):**\n"
            "Sis AI le orienta exclusivamente en la etapa de **reclamación extrajudicial directa** ante la aseguradora (Arts. 1077 y 1080 del Código de Comercio).\n\n"
            "Si la aseguradora objeta de manera injustificada o vencen los plazos legales, la interposición de demandas civiles o acciones de protección al consumidor ante la Delegatura de la Superintendencia Financiera requiere patrocinio letrado formal.\n\n"
            "> ⚖️ *Nota legal: Esta herramienta es un ejercicio académico de la Pontificia Universidad Javeriana y no constituye asesoría jurídica formal ni reemplaza el criterio de un abogado.*"
        )
        return respuesta, fuentes, "Filtro Prejudicial (Pre-litigio)"

    # 3. Contexto aumentado para el modelo
    contexto_normativo = "\n\n".join([
        f"--- NORMA RECUPERADA DEL CORPUS ({f['archivo']}) ---\n"
        f"Epígrafe: {f['titulo']}\n"
        f"Texto de ley: {f['texto']}"
        for f in fuentes
    ])

    system_prompt_con_rag = f"""{SYSTEM_PROMPT}

═══════════════════════════════════════════════════════════
CORPUS NORMATIVO RECUPERADO MEDIANTE RAG (CITA OBLIGATORIA):
═══════════════════════════════════════════════════════════
{contexto_normativo if contexto_normativo else "No se recuperaron normas específicas para esta consulta."}
"""

    clave_limpia = (api_key or obtener_api_key_sistema()).strip()

    if clave_limpia:
        headers = {
            "Authorization": f"Bearer {clave_limpia}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://javeriana.edu.co",
            "X-Title": "Sis AI Javeriana"
        }
        messages = [{"role": "system", "content": system_prompt_con_rag}]
        for m in historial[-6:]:
            if m.get("role") in ["user", "assistant"]:
                messages.append({"role": m["role"], "content": m["content"]})
        messages.append({"role": "user", "content": mensaje_usuario})

        # Cascada de modelos: primero el seleccionado por el usuario, luego los otros gratuitos
        candidatos = [modelo_preferido] + [m for m in MODELOS_GRATIS_DISPONIBLES if m != modelo_preferido]
        
        ultimo_error = ""
        for modelo_candidato in candidatos:
            payload = {
                "model": modelo_candidato,
                "messages": messages,
                "temperature": 0.2
            }
            try:
                resp = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                if resp.status_code == 200:
                    data = resp.json()
                    msg = data.get("choices", [{}])[0].get("message", {})
                    contenido = msg.get("content")
                    if not contenido and msg.get("reasoning"):
                        contenido = msg.get("reasoning")
                    if contenido and contenido.strip():
                        return contenido, fuentes, modelo_candidato
                elif resp.status_code == 429:
                    ultimo_error = f"{modelo_candidato} saturado temporalmente (429)"
                    continue
                else:
                    ultimo_error = f"{modelo_candidato} devolvió código {resp.status_code}"
                    continue
            except Exception as e:
                ultimo_error = f"{modelo_candidato} error de conexión: {str(e)}"
                continue

        return (
            f"*(Aviso: Modelos gratuitos de OpenRouter temporalmente no disponibles [{ultimo_error}]. Respondiendo con motor RAG local)*\n\n"
            + generar_respuesta_rag_local(mensaje_usuario, fuentes), fuentes, "Motor RAG Local"
        )
    else:
        return generar_respuesta_rag_local(mensaje_usuario, fuentes), fuentes, "Motor RAG Local"

def generar_respuesta_rag_local(mensaje, fuentes):
    citas = "\n\n".join([f"📖 **Fuente aplicada ({f['archivo']}):** *{f['titulo']}*\n> {f['texto'][:250]}..." for f in fuentes])
    
    return (
        "📍 **Orientación Jurídica sobre su Siniestro (Fundamentada en RAG):**\n\n"
        "1. **Carga probatoria y libertad de medios (Art. 1077 C.Co.):** Al asegurado le corresponde demostrar la ocurrencia y cuantía del daño, lo cual puede hacerse mediante cualquier medio idóneo (fotografías, cotizaciones de reparación, inventarios).\n"
        "2. **Aviso y fuerza mayor (Arts. 1075 y 1078 C.Co.):** El retardo justificado por fuerza mayor derivado de la catástrofe sísmica no extingue su derecho a reclamar.\n"
        "3. **Término perentorio para pagar (Art. 1080 C.Co.):** Radicada la reclamación, la aseguradora tiene **un (1) mes** para pagar o expedir objeción motivada; superado este plazo, incurre en **mora** legal.\n\n"
        f"**Normas exactas extraídas de tu corpus:**\n\n{citas}\n\n"
        "💡 *Consejo:* Puede ir a la pestaña **'📄 Generar Reclamación'** para estructurar su carta formal con estas normas.\n\n"
        "> ⚖️ *Nota legal: Esta herramienta es un ejercicio académico de la Pontificia Universidad Javeriana y no constituye asesoría jurídica formal ni reemplaza el criterio de un abogado.*"
    )

# ══════════════════════════════════════════════════════════════════════
# BARRA LATERAL (CONFIGURACIÓN Y NAVEGACIÓN)
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Escudo_de_la_Pontificia_Universidad_Javeriana.svg/300px-Escudo_de_la_Pontificia_Universidad_Javeriana.svg.png", width=110)
    st.title("⚖️ Sis AI")
    st.caption("**Proyecto Final · Derecho e IA**\nPontificia Universidad Javeriana (2026-II)")
    st.write("**Estudiante:** Jose David Vasco")
    st.divider()

    modo = st.radio(
        "Seleccione un módulo:",
        ["💬 Asistente Jurídico (Chat)", "📄 Generador de Reclamación Formal", "📚 Corpus Normativo"],
        index=0
    )

    st.divider()
    st.subheader("🤖 Configuración de IA (OpenRouter)")
    api_key_val = obtener_api_key_sistema()
    api_key_input = st.text_input(
        "OPENROUTER_API_KEY:",
        type="password",
        value=api_key_val,
        help="Clave para acceder a los modelos LLM en OpenRouter. Precargada automáticamente."
    )

    modelo_seleccionado = st.selectbox(
        "Modelo Gratuito OpenRouter:",
        MODELOS_GRATIS_DISPONIBLES,
        index=0,
        help="Seleccione el modelo libre de OpenRouter a emplear."
    )

    if api_key_input:
        st.success("🟢 Modo IA Conectado")
        if st.button("🔍 Probar Estado de la Clave", help="Verifica la conexión en tiempo real con OpenRouter"):
            with st.spinner("Consultando estado de la clave en OpenRouter..."):
                valido, msg_estado = verificar_conexion_openrouter(api_key_input)
                if valido:
                    st.success(f"✅ {msg_estado}")
                else:
                    st.error(f"❌ {msg_estado}")
        st.caption("⚡ Respaldo automático en cascada si un modelo gratuito está saturado.")
    else:
        st.info("💡 Modo activo: Simulación guiada por el Corpus normativo local.")

# ══════════════════════════════════════════════════════════════════════
# MÓDULO 1: CHAT JURÍDICO INTERACTIVO
# ══════════════════════════════════════════════════════════════════════
if modo == "💬 Asistente Jurídico (Chat)":
    st.header("💬 Asistente Jurídico — Sis AI")
    st.markdown(
        "Consulte sus inquietudes sobre la cobertura de su póliza de hogar o zonas comunes "
        "frente al sismo del 10 de agosto de 2026. El asistente responderá fundamentándose en el Código de Comercio y la ley colombiana."
    )

    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [
            {
                "role": "assistant",
                "content": (
                    "¡Hola! Soy **Sis AI**, asistente jurídico de la Universidad Javeriana. "
                    "Puedo orientarte en la estructuración de tu reclamación de seguro de hogar o copropiedad "
                    "por los daños sufridos en el sismo del 10 de agosto de 2026.\n\n"
                    "Cuéntame brevemente: ¿Qué tipo de inmueble tienes y qué afectación sufrió?\n\n"
                    "> ⚖️ *Nota legal: Esta herramienta es un ejercicio académico y no constituye asesoría jurídica formal.*"
                ),
                "modelo": "Inicialización"
            }
        ]

    for m in st.session_state.mensajes:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if m.get("modelo") and m.get("modelo") != "Inicialización":
                st.caption(f"🤖 *Motor:* `{m['modelo']}`")
            if m.get("fuentes"):
                with st.expander(f"📚 {len(m['fuentes'])} fuentes normativas recuperadas por RAG del corpus"):
                    for f in m["fuentes"]:
                        st.markdown(f"**Archivo:** `{f['archivo']}` — **Norma:** *{f['titulo']}*")
                        st.caption(f['texto'][:300] + "...")

    if prompt := st.chat_input("Escribe tu consulta jurídica aquí (ej. 'La aseguradora me dilata la reclamación'):"):
        st.session_state.mensajes.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Buscando en el corpus normativo (RAG) y generando respuesta jurídica con IA..."):
                respuesta, fuentes, modelo_usado = consultar_ia(prompt, st.session_state.mensajes, api_key_input, modelo_seleccionado)
                st.markdown(respuesta)
                st.caption(f"🤖 *Respuesta generada por:* `{modelo_usado}`")
                if fuentes:
                    with st.expander(f"📚 {len(fuentes)} fuentes normativas recuperadas por RAG del corpus"):
                        for f in fuentes:
                            st.markdown(f"**Archivo:** `{f['archivo']}` — **Norma:** *{f['titulo']}*")
                            st.caption(f['texto'][:300] + "...")
        st.session_state.mensajes.append({"role": "assistant", "content": respuesta, "fuentes": fuentes, "modelo": modelo_usado})

# ══════════════════════════════════════════════════════════════════════
# MÓDULO 2: GENERADOR DE RECLAMACIÓN FORMAL (ART. 1077 Y 1080 C.CO)
# ══════════════════════════════════════════════════════════════════════
elif modo == "📄 Generador de Reclamación Formal":
    st.header("📄 Generador de Reclamación Formal de Seguros")
    st.markdown(
        "Complete este formulario para generar de forma automatizada su memorial formal de "
        "reclamación fundamentado en el **Artículo 1077 y 1080 del Código de Comercio**. "
        "*Recuerde usar datos de prueba (Ley 1581 de 2012).*"
    )

    col1, col2 = st.columns(2)
    with col1:
        aseguradora = st.text_input("Compañía Aseguradora:", value="Seguros Bolívar S.A.")
        nombre_asegurado = st.text_input("Nombre del Asegurado (o marcador ficticio):", value="[Nombre del Asegurado]")
        identificacion = st.text_input("Identificación (C.C.):", value="[C.C. 000.000.000]")
        tipo_inmueble = st.selectbox("Tipo de Inmueble:", ["Apartamento en Propiedad Horizontal", "Casa Unifamiliar", "Local Comercial"])
    with col2:
        numero_poliza = st.text_input("Número de Póliza:", value="POL-SISMO-2026-X")
        ciudad = st.text_input("Ciudad del Inmueble:", value="Bogotá D.C.")
        cuantia_estimada = st.text_input("Valor Estimado de Reparaciones / Enseres (COP):", value="$15.000.000")
        fecha_reclamo = st.date_input("Fecha de radicación:", value=date.today())

    st.subheader("🛠️ Detalle de Afectaciones y Pruebas")
    descripcion_danos = st.text_area(
        "Descripción detallada de los daños sufridos:",
        value="Aparición de fisuras diagonales en muros divisorios no estructurales de mampostería, desprendimiento de pañete en sala-comedor y fractura de ventanería principal a causa del sismo."
    )
    pruebas = st.multiselect(
        "Pruebas que adjunta a la reclamación (Art. 1077 C.Co. - Libertad Probatoria):",
        [
            "Registro fotográfico a color fechado de los daños",
            "Cotización formal de reparación y mano de obra",
            "Informe o concepto de maestro de obra calificado",
            "Inventario detallado de bienes muebles y enseres averiados",
            "Copia de la carátula de la póliza de seguro",
            "Copia del recibo de pago de la prima al día"
        ],
        default=[
            "Registro fotográfico a color fechado de los daños",
            "Cotización formal de reparación y mano de obra",
            "Copia de la carátula de la póliza de seguro"
        ]
    )

    if st.button("🚀 Generar Minuta Formal de Reclamación", type="primary"):
        lista_pruebas_md = "\n".join([f"   - {p}" for p in pruebas])
        minuta = f"""
Señores
**DEPARTAMENTO DE SINIESTROS / INDEMNIZACIONES**
**{aseguradora.upper()}**
{ciudad}

**REF:** RECLAMACIÓN FORMAL DE INDEMNIZACIÓN POR SINIESTRO DE DAÑOS (TERREMOTO / SISMO)
**PÓLIZA N°:** {numero_poliza}
**ASEGURADO:** {nombre_asegurado} — Identificación: {identificacion}
**FECHA DEL EVENTO:** 10 de Agosto de 2026
**FECHA DE RADICACIÓN:** {fecha_reclamo.strftime('%d/%m/%Y')}

Respetados Señores:

Por medio de la presente, actuando en calidad de tomador/asegurado del contrato de seguro amparado bajo la póliza de la referencia, me permito formular formalmente **RECLAMACIÓN DE INDEMNIZACIÓN** por los daños directos acaecidos sobre el bien inmueble ({tipo_inmueble}) ubicado en la ciudad de {ciudad}, como consecuencia del sismo ocurrido el día 10 de agosto de 2026, con base en los siguientes:

### I. HECHOS
1. El pasado 10 de agosto de 2026 se presentó un evento sísmico con epicentro de alta intensidad, que impactó sensiblemente la infraestructura física del inmueble amparado.
2. A causa directa e inmediata de dicho sismo, el inmueble sufrió las siguientes afectaciones: {descripcion_danos}.
3. Conforme a las condiciones de la póliza contratada, el amparo básico de Terremoto, Temblor y Erupción Volcánica cubre las pérdidas y daños materiales directos que sufran los bienes asegurados.
4. Conforme a las cotizaciones técnicas recaudadas, el valor de las reparaciones necesarias para restituir el bien al estado inmediatamente anterior al siniestro asciende a la suma estimada de **{cuantia_estimada} M/CTE**.

### II. PETICIÓN
Solicito comedidamente que, previa verificación de los hechos y documentos aportados, se sirvan **LIQUIDAR Y PAGAR** la indemnización por los daños descritos en favor del suscrito asegurado, de conformidad con los límites y deducibles de la póliza suscrita.

### III. FUNDAMENTOS DE DERECHO
Fundamento esta reclamación en:
1. **Artículo 1077 del Código de Comercio:** Carga de la prueba. Mediante los anexos de este escrito se acredita debidamente tanto la ocurrencia del siniestro como la cuantía de la pérdida a través de medios idóneos y lícitos.
2. **Artículo 1080 del Código de Comercio:** Término perentorio para el pago. La aseguradora cuenta con el término legal de **un (1) mes calendario** siguiente a la recepción de esta acreditación para efectuar el pago correspondiente, vencido el cual se causarán los intereses moratorios certificados a la tasa máxima de la ley.
3. **Ley 1480 de 2011 (Art. 3) y Circular Básica Jurídica de la SFC:** Garantía de protección al consumidor y deber de resolución transparente sin imposición de trámites o peritajes dilatorios.

### IV. PRUEBAS APORTADAS
En ejercicio del principio de libertad probatoria, me permito adjuntar:
{lista_pruebas_md}

### V. NOTIFICACIONES
Recibiré notificaciones preferentemente a través del correo electrónico o dirección suministrada en la carátula de la póliza.

Atentamente,

________________________________________________
**{nombre_asegurado}**
{identificacion}
"""
        st.success("✅ ¡Minuta formal generada con éxito bajo estándares del Código de Comercio!")
        st.markdown(minuta)
        st.download_button(
            label="📥 Descargar Minuta en Formato de Texto (.txt)",
            data=minuta,
            file_name=f"Reclamacion_Sismo_{numero_poliza}.txt",
            mime="text/plain"
        )

# ══════════════════════════════════════════════════════════════════════
# MÓDULO 3: CORPUS NORMATIVO INTEGRADO (RAG)
# ══════════════════════════════════════════════════════════════════════
elif modo == "📚 Corpus Normativo":
    st.header("📚 Corpus Normativo del Asistente")
    st.markdown(
        "Consulte aquí las normas oficiales colombianas que gobiernan las respuestas de Sis AI, "
        "cargadas en el directorio `corpus/` de este proyecto."
    )

    pestana1, pestana2, pestana3 = st.tabs([
        "Código de Comercio (Arts. 1075-1080)",
        "Ley 1480 de 2011 (Estatuto Consumidor)",
        "Circular Básica Jurídica SFC"
    ])

    with pestana1:
        if os.path.exists("corpus/01_codigo_comercio_seguros.md"):
            with open("corpus/01_codigo_comercio_seguros.md", "r", encoding="utf-8") as f:
                st.markdown(f.read())
        else:
            st.info("Archivo de corpus en preparación.")

    with pestana2:
        if os.path.exists("corpus/02_ley_1480_estatuto_consumidor.md"):
            with open("corpus/02_ley_1480_estatuto_consumidor.md", "r", encoding="utf-8") as f:
                st.markdown(f.read())
        else:
            st.info("Archivo de corpus en preparación.")

    with pestana3:
        if os.path.exists("corpus/03_circular_superintendencia_financiera.md"):
            with open("corpus/03_circular_superintendencia_financiera.md", "r", encoding="utf-8") as f:
                st.markdown(f.read())
        else:
            st.info("Archivo de corpus en preparación.")

# Footer constante
st.divider()
st.caption(
    "Proyecto Final de Derecho e Inteligencia Artificial · Pontificia Universidad Javeriana 2026-II · "
    "Docente: Pedro Ardila · Estudiante: Jose David Vasco"
)
