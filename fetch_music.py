import random
from datetime import datetime
from ytmusicapi import YTMusic


def update_readme_playlist():
    # Initialisation en mode public (sans aucun compte ni cookie)
    ytmusic = YTMusic()

    print("🔍 Récupération des tendances publiques...")
    charts = ytmusic.get_charts(country="FR")
    all_trending = charts.get("videos", {}).get("items", [])[:50]
    
    # Filtrage des morceaux valides
    valid_tracks = [item for item in all_trending if "videoId" in item]

    # Tirage au sort de 15 titres
    sample_size = min(15, len(valid_tracks))
    selected_tracks = random.sample(valid_tracks, sample_size)

    today = datetime.now().strftime("%d/%m/%Y")

    # Génération du contenu Markdown
    content = f"# 🎧 Ma Playlist Découverte du Jour ({today})\n\n"
    content += "15 morceaux piochés automatiquement chaque matin dans le Top 50 des tendances France :\n\n"

    for index, item in enumerate(selected_tracks, start=1):
        title = item.get("title", "Titre inconnu")
        artists = ", ".join([a["name"] for a in item.get("artists", [])])
        video_id = item.get("videoId")
        url = f"https://music.youtube.com/watch?v={video_id}"

        content += f"{index}. **[{title}]({url})** — *{artists}*\n"

    content += "\n---\n*Mis à jour automatiquement chaque jour via GitHub Actions 🤖*"

    # Écriture dans le README.md
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Fichier README.md mis à jour avec succès !")


if __name__ == "__main__":
    update_readme_playlist()