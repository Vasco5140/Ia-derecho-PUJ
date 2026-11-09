# 📚 Hito M3 — Corpus Conectado y Arquitectura RAG

**Proyecto:** Sis AI — Asesoría legal sobre vivienda y sismos  
**Estudiante:** Jose David Vasco  
**Materia:** Derecho e Inteligencia Artificial · Pontificia Universidad Javeriana  
**Docente:** Pedro Ardila  

---

## 🎯 1. ¿Qué es RAG y por qué es vital para el Derecho?

**RAG (*Retrieval-Augmented Generation* o Generación Aumentada por Recuperación)** es la técnica que evita que los modelos de inteligencia artificial "alucinen" o inventen leyes.

En lugar de pedirle al modelo que responda según lo que "recuerda" de su entrenamiento general, el sistema RAG realiza un proceso en 3 pasos:
1. **Recuperación (*Retrieve*):** Toma la duda del usuario y busca en los archivos del directorio `corpus/` únicamente los fragmentos normativos relevantes (ej. artículos exactos del Código de Comercio).
2. **Aumento (*Augment*):** Inyecta esos fragmentos normativos dentro de la instrucción oculta que se le envía a la IA, diciéndole: *"Responde ÚNICAMENTE citando este fragmento legal que te acabo de entregar"*.
3. **Generación (*Generate*):** El modelo redacta la respuesta para el usuario, citando textualmente el artículo y la ley de donde extrajo el fundamento.

```
                      ┌──────────────────────────────────────┐
                      │    Directorio /corpus                │
                      │  - 01_codigo_comercio_seguros.md     │
                      │  - 02_ley_1480_estatuto_consumidor   │
                      │  - 03_circular_superfinanciera       │
                      └──────────────────┬───────────────────┘
                                         │
[Consulta del usuario] ──► [Motor de Búsqueda RAG] ──► [Fragmentos Legales Relevantes]
                                                                  │
                                                                  ▼
[Respuesta con Cita Exacta] ◄── [Modelo LLM] ◄── [Prompt + Fragmentos Inyectados]
```

---

## 🏛️ 2. Estructura del Corpus Normativo Cargado (`corpus/`)

El corpus de Sis AI se compone de tres fuentes jurídicas públicas del ordenamiento colombiano, seleccionadas por su pertinencia para víctimas del sismo del 10/08/2026:

### 1. [`corpus/01_codigo_comercio_seguros.md`](file:///c:/Users/josed/Desktop/IA%20abogados/corpus/01_codigo_comercio_seguros.md)
* **Art. 1075 (Aviso de siniestro):** Fija la regla general de dar noticia a la aseguradora dentro de los 3 días siguientes.
* **Art. 1077 (Carga y libertad probatoria):** Al asegurado le corresponde probar ocurrencia y cuantía, admitiendo **cualquier medio probatorio legal** (fotos, cotizaciones, videos, inventarios).
* **Art. 1078 (Excepción por fuerza mayor):** Exime de penalidad o pérdida de indemnización el aviso extemporáneo originado en fuerza mayor o caso fortuito (ej. colapso de comunicaciones tras el sismo).
* **Art. 1080 (Término perentorio y mora):** Obligación legal de la aseguradora de pagar dentro del **mes siguiente** a la radicación de la prueba, so pena de pagar intereses moratorios aumentados en el 50%.

### 2. [`corpus/02_ley_1480_estatuto_consumidor.md`](file:///c:/Users/josed/Desktop/IA%20abogados/corpus/02_ley_1480_estatuto_consumidor.md)
* **Art. 3 (Derechos del consumidor financiero):** Derecho a la información transparente, veraz e idónea, derecho a la reparación integral y protección frente a cláusulas y prácticas abusivas de las aseguradoras.

### 3. [`corpus/03_circular_superintendencia_financiera.md`](file:///c:/Users/josed/Desktop/IA%20abogados/corpus/03_circular_superintendencia_financiera.md)
* **Circular Externa 029 de 2014 (Título IV, Cap. II):** Prohibición a las entidades aseguradoras de imponer trámites dilatorios o peritajes costosos a cargo exclusivo del asegurado. Exigencia de respuesta escrita y motivada.

---

## ⚙️ 3. Implementación del Motor RAG en Sis AI

El motor RAG fue programado directamente en la aplicación web [`app.py`](file:///c:/Users/josed/Desktop/IA%20abogados/app.py) a través de los siguientes componentes:

1. **Cargador e indexador de chunks:** Lee todos los archivos `.md` de la carpeta `corpus/` y los divide por secciones temáticas (Artículos y Títulos).
2. **Recuperador semántico / de palabras clave:** Compara los términos de la consulta del usuario (*ej. "mora", "peritaje", "plazo para pagar", "aviso tarde"*) con el índice del corpus y recupera los fragmentos con mayor relevancia.
3. **Inyección en el contexto:** El fragmento recuperado se envía al modelo con la instrucción estricta de citar la fuente.
4. **Trazabilidad visual en la interfaz:** La aplicación web muestra un panel desplegable: *"🔍 Fuentes del Corpus recuperadas por el RAG"*, permitiendo al usuario y al docente verificar qué artículos fundamentaron la respuesta.

---

## 🧪 4. Ejemplo Real de Recuperación y Cita

* **Consulta del usuario:**  
  *"¿Cuánto tiempo tiene la aseguradora para pagar y qué pasa si no responde?"*

* **Fragmento recuperado del corpus (`corpus/01_codigo_comercio_seguros.md`):**  
  > *`### Artículo 1080. Término para el pago de la indemnización y mora: El asegurador estará obligado a efectuar el pago del siniestro dentro del mes siguiente a la fecha en que el asegurado o beneficiario acredite su derecho... Vencido este plazo, reconocerá intereses moratorios...`*

* **Respuesta generada por el asistente (con cita obligatoria):**  
  > *"Conforme al **Artículo 1080 del Código de Comercio de Colombia**, la aseguradora cuenta con un plazo perentorio de **un (1) mes calendario** a partir del momento en que usted radique la acreditación del siniestro y su cuantía (Art. 1077 C.Co.). Si no paga ni objeta motivadamente en dicho plazo, incurre por ministerio de la ley en mora y deberá reconocer intereses moratorios al interés bancario corriente incrementado en una mitad (50%).*
  > 
  > ⚖️ *Nota legal: Esta herramienta es un ejercicio académico de la Pontificia Universidad Javeriana y no constituye asesoría jurídica formal ni reemplaza el criterio de un abogado."*

---

## 🛡️ 5. Salvaguarda Anti-Alucinación

Si la consulta del usuario versa sobre temas ajenos al corpus normativo cargado (por ejemplo, subsidios de vivienda del Estado, multas de tránsito o impuestos), el motor RAG detecta la ausencia de coincidencias en el corpus y el modelo activa su regla de contención:

> *"No dispongo de información o fuente normativa sobre este punto en mi corpus."*

De esta manera se cumple con total rigor el mandato del **Hito M3** y la **Parte 6 del curso**.
