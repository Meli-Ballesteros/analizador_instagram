import os
import instaloader
from dotenv import load_dotenv

load_dotenv()

insta_user = os.getenv("INSTA_USER")
session_id = os.getenv("INSTA_SESSIONID")

if not insta_user or not session_id:
    print("❌ Error: Verifica INSTA_USER e INSTA_SESSIONID en tu archivo .env")
else:
    L = instaloader.Instaloader()
    
    # Extraer el ID numérico de usuario guardado en el primer segmento del sessionid
    ds_user_id = session_id.split('%')[0] if '%' in session_id else session_id.split(':')[0]
    
    # Asignar las cookies mínimas requeridas por Instaloader
    L.context._session.cookies.set('sessionid', session_id, domain='.instagram.com')
    L.context._session.cookies.set('ds_user_id', ds_user_id, domain='.instagram.com')
    
    # Marcar el contexto como autenticado
    L.context.username = insta_user
    
    # Guardar sesión local
    L.save_session_to_file(insta_user)
    print(f"✅ ¡Sesión validada y guardada con éxito para @{insta_user}!")