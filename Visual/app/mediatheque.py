import streamlit as st
import sqlite3
from pytube import YouTube

def mediatheque():
    # Se connecter à la base de données
    conn = sqlite3.connect('videos.db')
    c = conn.cursor()

    # Créer la table pour stocker les informations de la vidéo
    c.execute('''CREATE TABLE IF NOT EXISTS videos
                 (url text, title text, video_id text, likes integer NOT NULL DEFAULT 0, dislikes integer NOT NULL DEFAULT 0)''')
    conn.commit()

    # Créer la table pour stocker les informations de la vidéo
    c.execute('''CREATE TABLE IF NOT EXISTS favorites
                     (title text, author text, video_id text)''')
    conn.commit()

    # Demander à l'utilisateur de saisir une URL YouTube
    url = st.text_input('Entrez l\'URL de la vidéo YouTube:')

    #### ajouter controle pour slmt accepter youtube
    #### ajouter plus d'etapes
    #### utiliser st.form button pour les etapes

    # Si l'URL est valide, extraire les informations de la vidéo et les stocker dans la base de données
    if url:
        try:
            # Extraire les informations de la vidéo YouTube
            video = YouTube(url)
            title = video.title
            video_id = video.video_id
            likes = 0
            dislikes = 0

            # Stocker les informations de la vidéo dans la base de données
            c.execute("INSERT INTO videos VALUES (?, ?, ?, ?, ?)", (url, title, video_id, likes, dislikes))
            conn.commit()

            # Afficher la vidéo dans un IFrame
            st.write(f'### {title}')
            st.write(f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>', unsafe_allow_html=True)

            # Ajouter un lien pour rediriger vers la page YouTube de la vidéo
            st.write(f'[Regarder sur YouTube](https://www.youtube.com/watch?v={video_id})')

        except Exception as e:
            st.error('Une erreur est survenue lors de l\'extraction de la vidéo: Nous n\'acceptons que les vidéos Youtube. Il est possible que votre lien soit obsolète.')

    # Afficher la liste des vidéos dans la base de données
    c.execute("SELECT url, title, video_id, likes, dislikes FROM videos")
    rows = c.fetchall()
    st.write('### Liste des vidéos:')

    #Boutons sous la vidéo
    for i, row in enumerate(reversed(rows)):
        # Extraire les informations de la vidéo
        url = row[0]
        title = row[1]
        video_id = row[2]
        likes = row[3]
        dislikes = row[4]

        st.write(
            f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{row[2]}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>',
            unsafe_allow_html=True)

        col_fav, col_like, col_dislike, col4 = st.columns([2, 2, 2, 8])

        with col_fav:
            if st.button(f"\u2605", key=f"add-to-favorites-{i}"):
                # Ajouter la vidéo à la liste des favoris
                c.execute("INSERT INTO favorites VALUES (?, ?, ?)", (row[0], row[1], row[2]))
                conn.commit()
                st.write("**La vidéo a bien été ajoutée à vos favoris!**", unsafe_allow_html=True)

        with col_like:
            c.execute("SELECT likes FROM videos WHERE video_id = ?", (video_id,))
            result = c.fetchone()
            if result is not None:
                likes = result[0]
                st.write(f'Likes : {likes}')
            if st.button(f"\U0001F44D", key=f"like-{i}"):
                # Ajouter un like à la vidéo
                c.execute("UPDATE videos SET likes = likes + 1 WHERE video_id = ?", (video_id,))
                conn.commit()
                st.experimental_rerun()

        with col_dislike:
            c.execute("SELECT dislikes FROM videos WHERE video_id = ?", (video_id,))
            result = c.fetchone()
            if result is not None:
                dislikes = result[0]
                st.write(f'Dislikes : {dislikes}')
            if st.button(f"\U0001F44E", key=f"dislike-{i}"):
                # Ajouter un dislike à la vidéo
                c.execute("UPDATE videos SET dislikes = dislikes + 1 WHERE video_id = ?", (video_id,))
                conn.commit()
                st.experimental_rerun()

        with col4:
            if st.button(f"dev-btn: Retirer video", key=f"dev-btn-{i}"):
                # Retirer la vidéo à la liste des favoris
                c.execute("DELETE FROM videos WHERE video_id = ?", (video_id,))
                conn.commit()
                # Rafraîchir la page
                st.experimental_rerun()

mediatheque()