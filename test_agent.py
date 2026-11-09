"""
Script de prueba automatizada del Agente Sis AI con OpenRouter y RAG.
Verifica la conectividad con la API de OpenRouter usando modelos gratuitos y el corpus legal.
"""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import requests
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY", "")
MODELOS_A_PROBAR = [
    "nvidia/nemotron-3.5-lightning:free",
    "openrouter/free",
    "liquid/lfm-2.5-2.6b:free",
    "liquid/lfm-3-1.7b:free",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "google/gemma-4-31b-it:free"
]

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

def recuperar_rag(consulta, top_k=2):
    chunks = cargar_corpus()
    consulta_lower = consulta.lower()
    palabras = [p for p in consulta_lower.replace("?", "").replace("¿", "").split() if len(p) > 3]
    puntuados = []
    for c in chunks:
        score = 0
        texto_completo = (c["titulo"] + " " + c["texto"] + " " + c["archivo"]).lower()
        for p in palabras:
            if p in texto_completo:
                score += 1
        if any(w in consulta_lower for w in ["aviso", "tarde", "días", "tiempo"]):
            if "1075" in c["titulo"] or "1078" in c["titulo"]:
                score += 4
        if any(w in consulta_lower for w in ["prueba", "fotos", "perito", "cuantía"]):
            if "1077" in c["titulo"]:
                score += 4
        if any(w in consulta_lower for w in ["pagar", "pago", "mora", "plazo", "mes"]):
            if "1080" in c["titulo"]:
                score += 4
        if score > 0:
            puntuados.append((score, c))
    puntuados.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in puntuados[:top_k]]

def probar_agente(pregunta):
    print(f"\n=======================================================")
    print(f"❓ PREGUNTA DEL CIUDADANO:\n   \"{pregunta}\"")
    print(f"=======================================================")
    
    fuentes = recuperar_rag(pregunta)
    print(f"📚 RAG recuperó {len(fuentes)} fuentes normativas del corpus:")
    for f in fuentes:
        print(f"   - [{f['archivo']}] {f['titulo']}")
        
    contexto = "\n\n".join([f"Norma: {f['titulo']}\nTexto: {f['texto']}" for f in fuentes])
    
    system_prompt = f"""Eres Sis AI, orientador jurídico de la Universidad Javeriana sobre seguros y sismos del 10/08/2026 en Colombia.
Reglas:
1. Incluye la nota legal académica al final.
2. Cita los artículos pertinentes del Código de Comercio (1075, 1077, 1078, 1080).
3. Si la pregunta no es sobre seguros/sismos, di 'No dispongo de información en mi corpus'.

Normas recuperadas por RAG:
{contexto}
"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://javeriana.edu.co",
        "X-Title": "Sis AI Javeriana Test"
    }
    
    for mod in MODELOS_A_PROBAR:
        print(f"\n🔄 Intentando generación con modelo: {mod}...")
        payload = {
            "model": mod,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": pregunta}
            ],
            "temperature": 0.2
        }
        try:
            resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=25)
            if resp.status_code == 200:
                data = resp.json()
                contenido = data["choices"][0]["message"]["content"]
                print(f"✅ RESPUESTA EXITOSA DE {mod}:")
                print("-" * 55)
                print(contenido)
                print("-" * 55)
                return True
            else:
                print(f"⚠️ Modelo {mod} respondió {resp.status_code}. Probando siguiente modelo...")
        except Exception as e:
            print(f"⚠️ Error conectando a {mod}: {e}. Probando siguiente modelo...")
            
    print("❌ Todos los modelos remotos fallaron.")
    return False

if __name__ == "__main__":
    print("⚖️ INICIANDO PRUEBA DEL AGENTE SIS AI (OPENROUTER FREE MODELS)")
    print(f"🔑 API Key configurada: {API_KEY[:10]}...{API_KEY[-4:]}")
    
    pregunta = "¿Cuánto tiempo tiene la aseguradora para pagarme después de radicar mis fotos y cotizaciones, y qué pasa si no paga?"
    exito = probar_agente(pregunta)
    if exito:
        print("\n🎉 ¡EL AGENTE DE IA ESTÁ 100% OPERATIVO CON OPENROUTER!")
    else:
        print("\n⚠️ No se pudo completar la prueba.")
