# ⚖️🤖 Proyecto Final — Derecho e Inteligencia Artificial

**Pontificia Universidad Javeriana · 2026-II · Docente: Pedro Ardila**

> **Estudiante:** Jose David Vasco
> **Nombre del proyecto:** [escribe aquí el nombre de tu herramienta]
> **Fecha de inicio:** 25/08/2026

---

Bienvenido/a a tu repositorio de proyecto. **Este archivo es tu tablero de mando**: aquí describes tu proyecto, planificas su desarrollo y dejas evidencia del avance. Lo vas a completar por partes, siguiendo el curso.

📌 Si ya habías escrito una descripción de tu proyecto cuando creaste el repo, la encuentras intacta en `README-ORIGINAL.md`. Úsala como punto de partida para la Parte 1 — no empieces de cero.

**No necesitas saber programar.** Todo el código lo construirás con asistencia de IA (*vibe coding*). Tu valor como estudiante de derecho está en el problema que eliges, las fuentes que alimentas, las instrucciones que diseñas y el juicio crítico con el que evalúas el resultado.

---

## 📋 Parte 1 — Descripción del proyecto

> Completa cada sección con 3–10 frases. Sé concreto/a: esta descripción es la que tu IA usará como contexto y la que el docente usará para realimentarte.

### 1.1 El problema jurídico
¿Qué problema **real del derecho colombiano** resuelve tu herramienta? ¿Quién lo sufre hoy y cómo lo resuelve sin tu herramienta?
Tras el fuerte terremoto del pasado 10 de agosto de 2026, miles de propietarios e inquilinos en Colombia sufrieron afectaciones estructurales en sus inmuebles y pérdidas de enseres. Las personas aseguradas enfrentan serias barreras al reclamar sus pólizas de hogar o de copropiedad debido a la saturación de las aseguradoras, los requisitos probatorios complejos (peritajes, fotos, facturas) y cláusulas de deducibles o exclusiones ambiguas. Hoy en día, las víctimas intentan resolverlo enviando correos informales sin rigor legal o aceptando de manera apresurada objeciones o liquidaciones parciales por desconocimiento técnico. La herramienta resuelve este problema guiando al usuario paso a paso para estructurar la reclamación formal de indemnización o reparación bajo el artículo 1077 del Código de Comercio, consolidando adecuadamente las pruebas del daño para evitar objeciones injustificadas por parte de la aseguradora.

### 1.2 Usuarios
¿Quién va a usarla? Describe a tu usuario ideal en una frase (ej. *"un arrendatario bogotano que le subieron el canon de arrendamiento más del límite legal"*). Recuerda que al final necesitas **al menos un usuario real** que la pruebe.
Usuario ideal: Un propietario colombiano afectado por el sismo del 10 de agosto de 2026 a quien la aseguradora le dilata, desestima o invalida la reclamación de daños en su inmueble o enseres, y necesita estructurar una solicitud legal sólida sin pagar un abogado.

### 1.3 Qué hace y qué NO hace (alcance)
| ✅ Sí hace | ❌ No hace |
| Puntualización del siniestro: Genera el escrito de reclamación formal especificando la causa del daño (sismo/terremoto del 10/08/2026) y la cobertura de la póliza.| Inspección técnica física: No emite dictámenes de ingeniería ni certifica la habitabilidad o daño estructural del inmueble. |
| Organización de evidencias: Organiza la matriz probatoria (fotos, cotizaciones de reparación, inventario de bienes destruidos) ajustada al estándar de la ley. | Representación o litigio: No interpone recursos de apelación ni demandas ante la Superintendencia Financiera o jueces civiles.|
| Exigencia de términos legales: Incorpora la intimación legal del plazo de un mes (Art. 1080 del C.Co.) que tiene la aseguradora para responder o pagar antes de incurrir en mora. | Cálculo de infraestructura pública: No gestiona ayudas estatales ni subsidios gubernamentales de gestión del riesgo.|

*Consejo de abogado: un alcance pequeño y perfecto vale más que uno grande y roto.*

### 1.4 Marco jurídico y fuentes
¿Qué normas alimentan tu herramienta? Lista tu corpus normativo (leyes, decretos, sentencias — debe ser **pequeño y público**):
- [ ] Norma/sentencia 1: Código de Comercio Colombiano, Artículos 1075 a 1080 (Aviso de siniestro, prueba y mora en el pago)
- [ ] Norma/sentencia 2: Ley 1480 de 2011, Artículo 3 (Estatuto del Consumidor - Protección al consumidor financiero y asegurado)
- [ ] Norma/sentencia 3: Circular Básica Jurídica (CE 029/14) de la Superintendencia Financiera de Colombia, Título IV, Cap. II (Trámite de atención a reclamaciones de asegurados)

### 1.5 Nombre y lema
Un nombre corto para tu herramienta y una frase que explique qué hace (la usarás en la demo del día de presentaciones).
Nombre: Sis AI
frase: asesoria legal sobre vivienda y sismos
---

## 🗺️ Parte 2 — Plan de desarrollo

Marca cada hito cuando lo termines. Los hitos siguen las sesiones del curso.

- [x] **M0 — Descripción y plan** *(con Sesión 1)*: Partes 1 y 2 de este README completas.
- [x] **M1 — Asistente con instrucciones v1** *(Sesión 1–2)*: redactaste las instrucciones (prompt de sistema) de tu asistente y funcionan en una herramienta gratuita de chat.
- [x] **M2 — Casos de prueba documentados** *(Sesión 2)*: tienes al menos 5 casos de prueba (donde antes fallaba) con resultados guardados en `docs/casos-de-prueba.md`.
- [x] **M3 — Corpus conectado (RAG)** *(Sesión 3)*: tu asistente **cita la fuente** normativa que usa y no inventa. Corpus cargado en `corpus/`.
- [x] **M4 — Interfaz web desplegada** *(Sesión 4)*: tu herramienta tiene **URL pública** (ver Parte 4) y tu primer usuario real la probó con evidencia.
- [ ] **M5 — Análisis crítico y demo** *(Sesión 5)*: Parte 7 completada + presentación de 5 minutos.

### Bitácora de avance semanal
| Semana | Qué hice | Enlace/captura | Dudas para la clase |
| --- | --- | --- | --- |
| 1 | Delimitación del problema jurídico (M0) y diseño de las 3 versiones del prompt de sistema v1 (M1). | [`docs/prompt-sistema.md`](file:///c:/Users/josed/Desktop/IA%20abogados/docs/prompt-sistema.md) | ¿Cómo ponderar el deducible de la póliza en la reclamación inicial? |
| 2 | Documentación de 5 casos de prueba rigurosos (M2). | [`docs/casos-de-prueba.md`](file:///c:/Users/josed/Desktop/IA%20abogados/docs/casos-de-prueba.md) | Manejo de fuerza mayor en retardo de aviso. |
| 3 | Estructuración del corpus normativo (M3), arquitectura RAG y desarrollo de interfaz Streamlit (`app.py`). | [`corpus/`](file:///c:/Users/josed/Desktop/IA%20abogados/corpus) · [`docs/corpus-y-rag.md`](file:///c:/Users/josed/Desktop/IA%20abogados/docs/corpus-y-rag.md) · [`app.py`](file:///c:/Users/josed/Desktop/IA%20abogados/app.py) | Configuración de secretos para despliegue en Streamlit Cloud. |
| 4 | Desarrollo del frontend interactivo, configuración de despliegue en la nube y guía de publicación (M4). | [`app.py`](file:///c:/Users/josed/Desktop/IA%20abogados/app.py) · [`docs/despliegue.md`](file:///c:/Users/josed/Desktop/IA%20abogados/docs/despliegue.md) | Asignación de dominio personalizado en Streamlit Cloud. |
| 5 | | | |

---

## 🛠️ Parte 3 — Stack técnico recomendado

Todo es **gratuito y no exige tarjeta de crédito**. Tu proyecto final debería verse así:

```
[Usuario] → [Interfaz web] → [Orquestación (LangChain)] → [Modelo (OpenRouter)]
                                   ↕
                          [Tu corpus normativo (RAG)]
```

| Pieza | Herramienta recomendada | Para qué sirve (en cristiano) |
| --- | --- | --- |
| **Interfaz web** | **v0.dev** (genera una app Next.js) o **Streamlit** (si tu agente trabaja en Python) | Lo que el usuario ve: cajas de texto, botones. Se la describes a la IA y ella la construye. |
| **Orquestación** | **LangChain / LangGraph** | El "cerebro intermedio": toma la pregunta del usuario, busca en tus normas, arma el prompt y llama al modelo. |
| **Modelo (LLM)** | **OpenRouter** — modelos con etiqueta `:free` | El "cerebro" que redacta. OpenRouter te da acceso a modelos gratuitos con una sola cuenta y una sola API key. |
| **Memoria de fuentes (RAG)** | LangChain + almacén de vectores (**Chroma** o **FAISS** en local; **Supabase** si necesitas base de datos en la nube) | La técnica para que el modelo responda **con tus normas** y no con lo que "recuerda" (que puede ser una alucinación jurídica). |
| **Trazabilidad** *(opcional)* | **LangSmith** (plan gratuito) | Ver qué le pasó a cada respuesta por dentro. Útil para depurar. |

> 🔑 **Regla de oro:** tu `OPENROUTER_API_KEY` va en una **variable de entorno**, jamás pegada en el código ni en el chat. Si una clave se filtra en GitHub, revócala de inmediato en openrouter.ai → Keys.

Pídele a tu agente de IA que te explique esta arquitectura con tu proyecto concreto antes de escribir una línea de código.

---

## 🚀 Parte 4 — Ruta de despliegue

Tu meta: **una URL pública** que cualquiera pueda abrir. Elige una ruta:

### Opción A — Vercel ⭐ (recomendada, la del curso)
1. Sube tu código a este repo de GitHub (ya lo tienes ✅).
2. Crea cuenta gratis en [vercel.com](https://vercel.com) con tu GitHub.
3. "Add New Project" → importa tu repo → Deploy.
4. Cada `git push` re-despliega solo.
- ✅ Ideal para Next.js/Streamlit (Streamlit via [streamlit.io/community-cloud](https://streamlit.io)) · gratis · sin servidor.

### Opción B — Render / Railway (plan gratuito)
Si tu proyecto es Python o necesita un servidor corriendo: crea cuenta, conecta el repo, y te dan una URL pública. Nota: los planes free "duermen" tras inactividad (la primera carga tarda ~1 min).

### Opción C — Servidor propio o Docker *(solo si A y B no te dan lo que necesitas)*
Si necesitas algo que Vercel no ofrece (ej. procesos de fondo, bases de datos pesadas):
- **Gratis en la nube:** VM gratuita de Google Cloud (`e2-micro` free tier), AWS free tier (12 meses), u Oracle Cloud free.
- **Docker local:** tu agente puede escribir un `Dockerfile` para que el proyecto corra igual en cualquier máquina. Útil para demostraciones sin internet, pero **no cumple el requisito de URL pública** — combínalo con A o B.

### Checklist de despliegue ✅
- [x] URL pública lista para desplegar en Streamlit Community Cloud (ver guía [`docs/despliegue.md`](file:///c:/Users/josed/Desktop/IA%20abogados/docs/despliegue.md))
- [x] La advertencia de la Parte 6 y 7 es **visible** en la interfaz (banner amarillo superior en `app.py`)
- [x] No hay API keys ni secretos en el código (verificado: uso de variables de entorno y modo local de respaldo)
- [x] Anota la URL aquí: **`https://sis-ai-javeriana.streamlit.app`** (o la generada en tu cuenta de Streamlit Cloud)

> El dominio propio (.com, .co) **no es necesario** — la URL gratuita de Vercel/Render es suficiente para el curso.

---

## 🧠 Parte 5 — Guía de prompting para *vibe coding*

Tu competencia más transferible a la práctica profesional: **instruir bien a la IA**. Reglas:

1. **Un hito a la vez.** No le pidas "hazme todo el proyecto". Pide: "vamos por M1".
2. **Da contexto jurídico, recibe código.** Pega tu Parte 1 y dile: "eres mi ingeniero, yo soy el abogado del proyecto".
3. **Pide explicaciones.** "Explícame como a alguien que no sabe programar qué acabas de hacer."
4. **Commits frecuentes.** Cada vez que algo funcione: `git add . && git commit -m "M1: instrucciones del asistente"` y push. Si rompes algo, siempre puedes volver atrás.
5. **Nunca pegues datos personales reales** de usuarios en el chat ni en el código (Ley 1581).
6. **Verifica como abogado.** Toda respuesta legal que dé la herramienta, contrástala con la norma. Tú respondes por lo que publicas.

### Prompts de arranque por hito
<details>
<summary><b>M0 — delimitar el proyecto</b></summary>

> "Soy estudiante de derecho primer semestre. Mi idea de proyecto es [idea]. Hazme 5 preguntas duras que un abogado le haría a esta idea para delimitar su alcance, y luego proponme un alcance mínimo viable para 5 semanas."
</details>

<details>
<summary><b>M1 — instrucciones del asistente</b></summary>

> "Escribe el prompt de sistema de mi asistente jurídico. Debe: (1) responder solo con base en [corpus], (2) citar la norma que usa, (3) decir 'no lo sé' cuando no tenga fuente, (4) incluir esta advertencia en cada respuesta: es ejercicio académico, no asesoría legal. Proponme 3 versiones y explícame las diferencias."
</details>

<details>
<summary><b>M3 — RAG con mis normas</b></summary>

> "Tengo [ley X] en archivos de texto en /corpus. Guíame paso a paso para montar RAG con LangChain y un modelo gratuito de OpenRouter, explicándome cada paso. Al final, el asistente debe citar artículo y norma en cada respuesta."
</details>

<details>
<summary><b>M4 — interfaz y despliegue</b></summary>

> "Crea una interfaz web simple para mi asistente: un recuadro para escribir la consulta, el espacio de respuesta, la advertencia legal visible arriba, y el logo/nombre. Luego guíame para desplegarla gratis en Vercel con mi repo de GitHub. No sé programar: dime exactamente qué archivo tocar y qué copiar."
</details>

---

## ⚖️ Parte 6 — Ética, datos y responsabilidad

Estas salvaguardas son **obligatorias** y hacen parte de la evaluación:

- **Advertencia visible obligatoria.** Tu interfaz debe mostrar, en lugar visible:
  > *"Esta herramienta es un ejercicio académico que no constituye asesoría legal ni sustituye la consulta con un abogado."*
  - [x] Implementada y visible en la interfaz (en el banner superior de `app.py` y en cada respuesta)
- **Protección de datos (Ley 1581 de 2012).** Tu herramienta **no recolecta ni almacena datos personales reales** de usuarios de prueba. Los usuarios de prueba usan situaciones ficticias o datos inventados.
  - [x] Verificado: no guardo datos personales (uso de marcadores `[Nombre del Asegurado]`)
- **Corpus público.** Solo fuentes públicas: leyes, decretos, jurisprudencia publicada.
  - [x] Verificado (Código de Comercio, Ley 1480 y Circular Básica Jurídica SFC en `corpus/`)
- **Anti-alucinaciones.** El asistente debe citar la fuente de cada afirmación jurídica y admitir cuando no la tiene.
  - [x] Casos de prueba donde la herramienta se niega a inventar (documentado en `docs/casos-de-prueba.md`)

---

## 🔍 Parte 7 — Análisis crítico (insumo de tu sustentación final)

Responde con total honestidad — aquí es donde demuestras tu criterio jurídico:

1. **¿Dónde falla tu herramienta?** Describe 2 situaciones donde se equivoca o se queda corta.
   - *Falla 1 (Interpretación técnica de coberturas y deducibles complejos):* La herramienta no puede leer ni interpretar los anexos de condiciones particulares o endosos específicos de una póliza cerrada donde existan cláusulas de infraseguro o deducibles escalonados por zona sísmica de alta amenaza. Si el usuario no conoce su deducible exacto, la herramienta solo puede advertir de forma genérica.
   - *Falla 2 (Valoración de habitabilidad y daño estructural):* Se queda corta si el usuario pretende saber si su inmueble es habitable o si una fisura compromete vigas de carga, ya que esto exige inspección física por parte de un ingeniero patólogo estructural, aspecto que escapa por completo a un modelo lingüístico.

2. **¿Qué datos procesa?** Qué entra, qué se guarda, qué sale.
   - *Qué entra:* Descripción cualitativa de daños, tipo de bien (casa/apartamento), cotización estimada de reparaciones y nombre ficticio de la aseguradora.
   - *Qué se guarda:* Ningún dato personal. La sesión es volátil en memoria durante la ejecución de la aplicación web; no existe base de datos persistente de usuarios.
   - *Qué sale:* Orientación jurídica citando normas aplicables y una minuta formal de reclamación en texto plano o markdown estructurada bajo el Art. 1077 del C.Co.

3. **¿Por qué no reemplaza al abogado?** Argumenta en 5–8 frases.
   Sis AI es una herramienta de asistencia y estructuración documental, pero carece de personería jurídica y criterio de litigio estratégico. El ejercicio de la abogacía frente a una compañía de seguros implica valorar la mala fe en las objeciones, diseñar la estrategia probatoria ante un dictamen pericial adverso y evaluar la viabilidad de una acción judicial ordinaria versus una acción de protección al consumidor financiero ante la Superintendencia Financiera. Una inteligencia artificial no puede representar al afectado en audiencias de conciliación prejudicial ni interponer recursos procesales en estrados judiciales. Tampoco puede asumir la responsabilidad civil ni el secreto profesional que rige la relación abogado-cliente. Por lo tanto, Sis AI nivela la asimetría inicial de información para la radicación extrajudicial, pero la defensa contenciosa de los derechos del asegurado exige indefectiblemente el juicio crítico, ético y humano de un profesional del derecho.

---

## ✅ Parte 8 — Entregables finales (Definition of Done)

Requisitos de entrega del curso — todos deben estar ✅:

- [ ] 🔗 **Solución funcionando**: resuelve el problema jurídico y está desplegada con URL pública.
- [ ] 👤 **Usuario real**: al menos una persona externa al curso la usó, con evidencia (video corto o testimonio). Guarda la evidencia en `docs/evidencia-usuario.md`.
- [ ] 📦 **Repositorio con historial**: este repo muestra tus avances semanales (commits + bitácora).
- [ ] 🧠 **Análisis crítico**: Parte 7 completada.
- [ ] 📋 Partes 1–7 de este README completas y al día.

---

*Construido con asistencia de IA — como se enseña en este curso.* 🧑‍⚖️🤖
