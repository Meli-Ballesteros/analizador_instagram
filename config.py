import os
from dotenv import load_dotenv

# Cargar las variables definidas en el archivo .env
load_dotenv()

# Obtener la API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("⚠️ No se encontró la GEMINI_API_KEY en el archivo .env")