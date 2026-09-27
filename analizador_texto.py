import json
import os
from dotenv import load_dotenv
from google import genai

# 1. Cargar obligatoriamente las variables del archivo .env primero
load_dotenv()

# 2. Pasar explícitamente la API Key al cliente
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def analizar_transcripcion(texto_transcripcion):
    print("🧠 Analizando la transcripción con Inteligencia Artificial...\n")

    prompt = f"""
    Eres un experto en estrategia de contenido para Instagram Reels y TikTok. 
    Analiza la siguiente transcripción de un Reel y extrae la información clave.

    Transcripción del Reel:
    \"\"\"{texto_transcripcion}\"\"\"

    Debes responder ÚNICAMENTE en formato JSON válido con la siguiente estructura:
    {{
        "hook": "El gancho o primera frase usada para captar la atención en los primeros 3 segundos",
        "tipo_de_hook": "Tipo de gancho (ej. Educativo, Problema/Solución, Curiosidad, Tutorial)",
        "puntos_clave": [
            "Punto o paso 1 mencionado en el video",
            "Punto o paso 2 mencionado en el video"
        ],
        "cta": "El llamado a la acción al final del video (si no hay, indica 'No especificado')",
        "tono": "Tono del mensaje (ej. Directo, Cercano, Profesional, Dinámico)",
        "resumen_ejecutivo": "Breve resumen de 2 frases sobre qué trata el Reel",
        "potencial_de_adaptacion": "Sugerencia de cómo adaptar esta estructura a otro nicho (ej. belleza, tecnología, producto)"
    }}
    """

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )

    texto_respuesta = response.text.strip()
    if texto_respuesta.startswith("```json"):
        texto_respuesta = (
            texto_respuesta.replace("```json", "").replace("```", "").strip()
        )

    try:
        resultado_json = json.loads(texto_respuesta)
        return resultado_json
    except json.JSONDecodeError:
        print("⚠️ No se pudo formatear como JSON, retornando texto plano:")
        return response.text


if __name__ == "__main__":
    transcripcion_ejemplo = (
        "Here's how I set up my home screen so that it's a productivity tool and not a distraction. "
        "I'll show you exactly how to create this home screen. The first thing you need to do is to create "
        "a reminder list for all of the days of the week, just like this. I combine Monday and Tuesday together "
        "because I have more things to do on the weekend, but you could combine Saturday and Sunday. You can "
        "also select different colors for each list or just add cute emojis just like I did. And then you're "
        "gonna press on your home screen and then click on edit and add a widget. And then just search reminders "
        "and then you can add your reminder list. And then just choose the day of the week and that's it. "
        "You'll place them and then just repeat this for each day of the week. And then you'll have separate "
        "to-do list on your home screen just like this."
    )

    analisis = analizar_transcripcion(transcripcion_ejemplo)

    print("📊 RESULTADO DEL ANÁLISIS:")
    print("===============================================")
    print(json.dumps(analisis, indent=4, ensure_ascii=False))
    print("===============================================")