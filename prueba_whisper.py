import whisper
import warnings

# Ocultar advertencias molestas de la terminal
warnings.filterwarnings("ignore")

def probar_transcripcion(ruta_video):
    print("🎙️ Cargando la Inteligencia Artificial de Whisper (modelo base)...")
    model = whisper.load_model("base")
    
    print(f"⏳ Escuchando y transcribiendo el video: {ruta_video}...")
    # Whisper extrae el audio directamente del mp4 y lo transcribe
    resultado = model.transcribe(ruta_video)
    
    texto = resultado["text"].strip()
    
    print("\n✅ ¡Transcripción completada!\n")
    print("=" * 40)
    print(texto)
    print("=" * 40)

if __name__ == "__main__":
    # Asegúrate de que el video descargado se llame así y esté en la misma carpeta
    video_real = "reel_prueba.mp4" 
    probar_transcripcion(video_real)