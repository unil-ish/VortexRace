import streamlit as st
import sqlite3
from pytube import YouTube

def mediatheque():
    # Se connecter à la base de données
    conn = sqlite3.connect('videos.db')
    c = conn.cursor()

    # Créer la table pour stocker les informations de la vidéo
    c.execute('''CREATE TABLE IF NOT EXISTS videos
                 (url text, title text, video_id text)''')
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

            # Stocker les informations de la vidéo dans la base de données
            c.execute("INSERT INTO videos VALUES (?, ?, ?)", (url, title, video_id))
            conn.commit()

            # Afficher la vidéo dans un IFrame
            st.write(f'### {title}')
            st.write(f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>', unsafe_allow_html=True)

            # Ajouter un lien pour rediriger vers la page YouTube de la vidéo
            st.write(f'[Regarder sur YouTube](https://www.youtube.com/watch?v={video_id})')

        except Exception as e:
            st.error('Une erreur est survenue lors de l\'extraction de la vidéo: Nous n\'acceptons que les vidéos Youtube. Il est possible que votre lien soit obsolète.')

    # Afficher la liste des vidéos dans la base de données
    c.execute("SELECT * FROM videos")
    rows = c.fetchall()
    st.write('### Liste des vidéos:')

    #Boutons sous la vidéo
    col_fav, col_like = st.beta_columns(2)
    for i, row in enumerate(reversed(rows)):
        st.write(
            f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{row[2]}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>',
            unsafe_allow_html=True)
        if st.button(f"\u2605", key=f"add-to-favorites-{i}"):
            # Ajouter la vidéo à la liste des favoris
            c.execute("INSERT INTO favorites VALUES (?, ?, ?)", (row[0], row[1], row[2]))
            conn.commit()
            st.write("**La vidéo a bien été ajoutée à vos favoris!**", unsafe_allow_html=True)

        if st.button(f"\U0001F44D", key=f"like-{i}"):
            # Ajouter un like à la vidéo
            #c.execute("INSERT INTO favorites VALUES (?, ?, ?)", (row[0], row[1], row[2]))
            #conn.commit()
            st.write("**+1**", unsafe_allow_html=True)

mediatheque()