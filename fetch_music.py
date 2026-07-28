import random
from datetime import datetime
from ytmusicapi import YTMusic


def update_readme_playlist():
    ytmusic = YTMusic()

    print("🔍 Récupération des tendances ou morceaux populaires...")
    valid_tracks = []

    # 1. Tentative de récupération via les charts
    try:
        charts = ytmusic.get_charts(country="FR")
        videos_data = charts.get("videos") or charts.get("trending")

        if isinstance(videos_data, dict):
            items = videos_data.get("items", [])
        elif isinstance(videos_data, list):
            items = videos_data
        else:
            items = []

        valid_tracks = [item for item in items if "videoId" in item]
    except Exception as e:
        print(f"⚠️ Erreur lors de la lecture des charts : {e}")

    # 2. Secours via la recherche si les charts ne renvoient pas de titres directement
    if not valid_tracks:
        print("💡 Utilisation de la recherche 'Top 50 France' en secours...")
        search_results = ytmusic.search(
            "Top 50 France", filter="songs", limit=50
        )
        valid_tracks = [item for item in search_results if "videoId" in item]

    # 3. Tirage au sort de 15 titres
    sample_size = min(15, len(valid_tracks))
    selected_tracks = random.sample(valid_tracks, sample_size)

    today = datetime.now().strftime("%d/%m/%Y")

    # 4. Génération du contenu Markdown
    content = f"# 🎧 Ma Playlist Découverte du Jour ({today})\n\n"
    content += "15 morceaux piochés automatiquement chaque matin dans les tendances France :\n\n"

    for index, item in enumerate(selected_tracks, start=1):
        title = item.get("title", "Titre inconnu")

        # Formatage des artistes
        artists_list = item.get("artists", [])
        if isinstance(artists_list, list):
            artists = ", ".join(
                [a.get("name", "") for a in artists_list if isinstance(a, dict)]
            )
        else:
            artists = "Artiste inconnu"

        video_id = item.get("videoId")
        url = f"https://music.youtube.com/watch?v={video_id}"

        content += f"{index}. **[{title}]({url})** — *{artists}*\n"

    content += "\n---\n*Mis à jour automatiquement chaque jour via GitHub Actions 🤖*"

    # 5. Écriture dans le README.md
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Fichier README.md mis à jour avec succès !")


if __name__ == "__main__":
    update_readme_playlist()