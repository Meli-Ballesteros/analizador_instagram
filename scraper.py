import instaloader
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv()

def obtener_top_reels(username: str, max_posts: int = 5):
    print(f"\n🔍 Conectando con Instagram para analizar a @{username}...")
    
    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        quiet=True
    )

    insta_user = os.getenv("INSTA_USER")

    if not insta_user:
        print("❌ Error: INSTA_USER no definido en .env")
        return None

    # Ruta exacta del archivo de sesión en la raíz del proyecto
    session_file = insta_user

    try:
        if os.path.exists(session_file):
            print(f"🔐 Cargando sesión guardada desde {session_file}...")
            # Forzar la lectura desde el archivo local del proyecto
            L.load_session_from_file(insta_user, filename=session_file)
            print("✅ Sesión cargada correctamente.")
        else:
            print(f"⚠️ No se encontró {session_file}. Ejecuta primero: python crear_sesion.py")
            return None
    except Exception as e:
        print(f"❌ Error al cargar la sesión: {e}")
        return None

    try:
        profile = instaloader.Profile.from_username(L.context, username)
    except Exception as e:
        print(f"❌ Error al acceder al perfil @{username}: {e}")
        return None

    posts_data = []
    print(f"📥 Obteniendo Reels de @{username}...")

    for post in profile.get_posts():
        if post.is_video:
            likes = post.likes
            comments = post.comments
            views = post.video_view_count if post.video_view_count else 1
            
            engagement_rate = round(((likes + comments) / views) * 100, 2)
            
            posts_data.append({
                'shortcode': post.shortcode,
                'date': post.date_local.strftime('%Y-%m-%d %H:%M'),
                'views': views,
                'likes': likes,
                'comments': comments,
                'engagement_rate': engagement_rate,
                'video_url': post.video_url,
                'caption': post.caption if post.caption else ""
            })
            
            print(f"  ✓ Reel obtenido [{post.shortcode}]: {views} vistas | ER: {engagement_rate}%")
            
            time.sleep(3)

            if len(posts_data) >= max_posts:
                break

    if not posts_data:
        print("⚠️ No se encontraron Reels en el perfil analizado.")
        return None

    df = pd.DataFrame(posts_data)
    return df.sort_values(by='engagement_rate', ascending=False)

if __name__ == "__main__":
    usuario_objetivo = "charlotte.arsenault"
    df_resultado = obtener_top_reels(usuario_objetivo, max_posts=3)
    if df_resultado is not None:
        print("\n🏆 Resultados:")
        print(df_resultado[['shortcode', 'views', 'likes', 'engagement_rate']])