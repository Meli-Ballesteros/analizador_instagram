import whisper
import requests
import os

# Carpeta para guardar los videos temporales
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def descargar_video(url: str, shortcode: str) -> str:
    """Descarga el MP4 del Reel para poder extraerle el audio."""
    file_path = os.path.join(DOWNLOAD_DIR, f"{shortcode}.mp4")
    
    if os.path.exists(file_path):
        return file_path

    print(f"📥 Descargando video del Reel [{shortcode}]...")
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("✅ Descarga completa.")
        return file_path
    else:
        print(f"❌ Error al descargar el video. Código HTTP: {response.status_code}")
        return None

def transcribir_audio(video_path: str) -> str:
    """Usa Whisper para pasar el audio del video a texto."""
    if not video_path:
        return ""
        
    print("🎙️ Cargando modelo Whisper (esto puede tardar unos segundos)...")
    model = whisper.load_model("base") # Usamos el modelo 'base' que es rápido
    
    print("⏳ Transcribiendo audio a texto...")
    result = model.transcribe(video_path)
    
    texto = result.get("text", "").strip()
    return texto

# Bloque de prueba (lo usaremos más adelante)
if __name__ == "__main__":
    print("Módulo transcriber.py listo para usarse.")