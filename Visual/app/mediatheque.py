import streamlit as st
import sqlite3
from pytube import YouTube
import logintests2

username = logintests2.get_logged_in_user()

"""
from loginWidgetStolen import __login__

myObject = __login__(auth_token = "courier_auth_token",
                    company_name = "Shims",
                    width = 200, height = 250,
                    logout_button_name = 'Logout', hide_menu_bool = False,
                    hide_footer_bool = False,)
username = myObject.get_username()"""

def mediatheque():
    # Se connecter à la base de données
    conn = sqlite3.connect('videos.db')
    c = conn.cursor()

    # Créer la table pour stocker les informations de la vidéo
    c.execute('''CREATE TABLE IF NOT EXISTS videos
                 (url text, title text, video_id text, likes integer NOT NULL DEFAULT 0, dislikes integer NOT NULL DEFAULT 0, liked_by, disliked_by, fav_by)''')
    conn.commit()

    """# Créer la table pour stocker les vidéos favorites (doit être perso, une pour chaque user)
    c.execute('''CREATE TABLE IF NOT EXISTS favorites
                     (title text, author text, video_id text)''')
    conn.commit()"""

    # Essais pour vider le st.text_input afin d'eviter les doublons
    # Enlever les "#" des ligns 36-37 39-40, puis essayer avec soit 42-43 soit 45-46 en ayant la ligne 49 en commentaire

    # if "my_text_input" not in st.session_state:
    #     st.session_state.my_text_input = ""
    #
    # def clear_text_input():
    #     st.session_state.my_text_input = ""

    # url = st.text_input('Entrez l\'URL de la vidéo YouTube:', value=st.session_state.my_text_input,
    #                                  on_change=clear_text_input, key="text_input")

    # url = st.text_input('Entrez l\'URL de la vidéo YouTube:',
    #                     on_change=clear_text_input, key="widget")

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
            title = ""
            video_id = video.video_id
            likes = 0
            dislikes = 0
            liked_by = ""
            disliked_by = ""
            fav_by = ""

            # Stocker les informations de la vidéo dans la base de données
            c.execute("INSERT INTO videos VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (url, title, video_id, likes, dislikes, liked_by, disliked_by, fav_by))
            conn.commit()

            # Afficher la vidéo dans un IFrame
            st.write(f'### {title}')
            st.write(f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>', unsafe_allow_html=True)

            # Ajouter un lien pour rediriger vers la page YouTube de la vidéo
            st.write(f'[Regarder sur YouTube](https://www.youtube.com/watch?v={video_id})')

        except Exception as e:
            st.write(e)
            st.error('Une erreur est survenue lors de l\'extraction de la vidéo: Nous n\'acceptons que les vidéos Youtube. Il est possible que votre lien soit obsolète.')
            st.error("Si vous êtes sûr de votre lien YouTube, réessayez.")

    # Afficher la liste des vidéos dans la base de données
    c.execute("SELECT url, title, video_id, likes, dislikes, liked_by, disliked_by, fav_by, (likes - dislikes) AS difference FROM videos ORDER BY difference DESC ")
    rows = c.fetchall()
    st.write('### Liste des vidéos:')

    #Boutons sous la vidéo
    for i, row in enumerate(rows):
        # Extraire les informations de la vidéo
        url = row[0]
        title = row[1]
        video_id = row[2]
        likes = row[3]
        dislikes = row[4]
        liked_by = row[5]
        disliked_by = row[6]
        fav_by = row[7]

        st.write(
            f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{row[2]}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>',
            unsafe_allow_html=True)

        col_fav, col_like, col_dislike, col4 = st.columns([2, 2, 2, 8])

        with col_fav:
            if st.button(f"\u2605", key=f"add-to-favorites-{i}"):
                # Ajouter la vidéo à la liste des favoris (ajout du username à fav_by)
                fav_by_list = fav_by.split(", ")
                if username not in fav_by_list:
                    fav_by_list.append(username)
                    fav_by = ", ".join(fav_by_list)
                    c.execute("UPDATE videos SET fav_by = ? WHERE video_id = ?", (fav_by, video_id,))
                    conn.commit()
                    st.write("**La vidéo a bien été ajoutée à vos favoris!**", unsafe_allow_html=True)
                else:
                    fav_by_list.remove(username)
                    fav_by = ", ".join(fav_by_list)
                    c.execute("UPDATE videos SET fav_by = ? WHERE video_id = ?", (fav_by, video_id,))
                    conn.commit()
                    st.write("**La vidéo a été retirée de vos favoris!**", unsafe_allow_html=True)

        with col_like:
            c.execute("SELECT likes, dislikes, liked_by, disliked_by FROM videos WHERE video_id = ?", (video_id,))
            result = c.fetchone()
            if result is not None:
                likes = result[0]
                st.write(f'Likes : {likes}')
                st.write(f'Liked by : {liked_by}')
            if st.button(f"\U0001F44D", key=f"like-{i}"):
                # Ajouter un like à la vidéo et le username à liked_by
                liked_by_list = liked_by.split(", ")
                disliked_by_list = disliked_by.split(", ")
                if username not in liked_by_list:
                    liked_by_list.append(username)
                    liked_by = ", ".join(liked_by_list)
                    c.execute("UPDATE videos SET likes = likes + 1, liked_by = ? WHERE video_id = ?", (liked_by, video_id,))
                    conn.commit()
                    if username in disliked_by_list:
                        disliked_by_list.remove(username)
                        disliked_by = ", ".join(disliked_by_list)
                        c.execute("UPDATE videos SET dislikes = dislikes - 1, disliked_by = ? WHERE video_id = ?",
                                  (disliked_by, video_id,))
                        conn.commit()
                else:
                    liked_by_list.remove(username)
                    liked_by = ", ".join(liked_by_list)
                    c.execute("UPDATE videos SET likes = likes - 1, liked_by = ? WHERE video_id = ?", (liked_by, video_id,))
                    conn.commit()
                st.experimental_rerun()

        with col_dislike:
            c.execute("SELECT likes, dislikes, liked_by, disliked_by FROM videos WHERE video_id = ?", (video_id,))
            result = c.fetchone()
            if result is not None:
                dislikes = result[1]
                st.write(f'Dislikes : {dislikes}')
                st.write(f'Disliked by : {disliked_by}')
            if st.button(f"\U0001F44E", key=f"dislike-{i}"):
                # Ajouter un dislike à la vidéo
                liked_by_list = liked_by.split(", ")
                disliked_by_list = disliked_by.split(", ")
                if username not in disliked_by_list:
                    disliked_by_list.append(username)
                    disliked_by = ", ".join(disliked_by_list)
                    c.execute("UPDATE videos SET dislikes = dislikes + 1, disliked_by = ? WHERE video_id = ?", (disliked_by, video_id,))
                    conn.commit()
                    if username in liked_by_list:
                        liked_by_list.remove(username)
                        liked_by = ", ".join(liked_by_list)
                        c.execute("UPDATE videos SET likes = likes - 1, liked_by = ? WHERE video_id = ?",
                                  (liked_by, video_id,))
                        conn.commit()
                else:
                    disliked_by_list.remove(username)
                    disliked_by = ", ".join(disliked_by_list)
                    c.execute("UPDATE videos SET dislikes = dislikes - 1, disliked_by = ? WHERE video_id = ?", (disliked_by, video_id,))
                    conn.commit()
                st.experimental_rerun()

        with col4:
            if st.button(f"dev-btn: Retirer video", key=f"dev-btn-{i}"):
                # Retirer la vidéo à la liste des favoris
                c.execute("DELETE FROM videos WHERE video_id = ?", (video_id,))
                conn.commit()
                # Rafraîchir la page
                st.experimental_rerun()

