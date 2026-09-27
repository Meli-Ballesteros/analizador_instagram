from google import genai
from config import GEMINI_API_KEY

def probar_entorno():
    print("Conectando con la API de Gemini...")
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Nombre actualizado del modelo solicitado por el SDK
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents="Responde únicamente: '¡Entorno listo para analizar Instagram!'"
    )
    
    print("\nRespuesta de la IA:")
    print(response.text)

if __name__ == "__main__":
    probar_entorno()