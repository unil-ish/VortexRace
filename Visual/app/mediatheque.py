import streamlit as st
import sqlite3
from pytube import YouTube
import main

# Get the logged in username
username = main.get_logged_in_user()

def mediatheque():
    # Connect to the videos database
    conn = sqlite3.connect('videos.db')
    c = conn.cursor()

    # Create the table to stock the videos
    c.execute('''CREATE TABLE IF NOT EXISTS videos
                 (url text, title text, video_id text, likes integer NOT NULL DEFAULT 0, dislikes integer NOT NULL DEFAULT 0, liked_by, disliked_by, fav_by)''')
    conn.commit()

    #Info message
    st.info(' ℹ️ Only Youtube videos can be added.')
    # Input asking the user to enter an url, to add the video
    url = st.text_input('Entrez l\'URL de la vidéo YouTube:')

    # If url valid, extract video informations and add the video to the database
    if url:

        # Check if url already in video db
        query = "SELECT * FROM videos WHERE url = ?"
        string_to_check = url

        c.execute(query, (string_to_check,))
        result = c.fetchone()

        # If url already in, erro message
        if result:
            st.error("Cette vidéo est déja dans la base de donnée")

        # If not, add the video to db
        else:
            try:
                # Extract informations
                video = YouTube(url)
                title = ""
                video_id = video.video_id
                likes = 0
                dislikes = 0
                liked_by = ""
                disliked_by = ""
                fav_by = ""

                # Insert the video into the database
                c.execute("INSERT INTO videos VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (url, title, video_id, likes, dislikes, liked_by, disliked_by, fav_by))
                conn.commit()

            # Send an error message if the link isn't valid (not a youtube video or else...)
            except Exception as e:
                st.write(e)
                st.error('Une erreur est survenue lors de l\'extraction de la vidéo: Nous n\'acceptons que les vidéos Youtube. Il est possible que votre lien soit obsolète.')
                st.error("Si vous êtes sûr de votre lien YouTube, réessayez.")

    # Select all the videos and order them by ratio of likes-dislikes
    c.execute("SELECT url, title, video_id, likes, dislikes, liked_by, disliked_by, fav_by, (likes - dislikes) AS difference FROM videos ORDER BY difference DESC ")
    rows = c.fetchall()
    st.write('### Liste des vidéos:')

    # Display all the videos
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

        # Frame code to display the video
        iframe_code = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{row[2]}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>'

        # Markdown to center the video
        st.markdown(
            """
            <style>
            .centered-content {
                display: flex;
                justify-content: center;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Display the video (centered)
        centered_iframe = f'<div class="centered-content">{iframe_code}</div>'
        st.markdown(centered_iframe, unsafe_allow_html=True)

        # Set columns for all the buttons (that are under each video)
        col1, col_fav, col_like, col_dislike, col4 = st.columns([3, 2, 2, 2, 1.7])

        # Button to add a video to user's favorites
        with col_fav:
            if st.button(f"\u2605", key=f"add-to-favorites-{i}"):
                # Add the username to fav_by_list if not already in
                fav_by_list = fav_by.split(", ")
                if username not in fav_by_list:
                    fav_by_list.append(username)
                    fav_by = ", ".join(fav_by_list)
                    # Update the database with the updated fav_by_list
                    c.execute("UPDATE videos SET fav_by = ? WHERE video_id = ?", (fav_by, video_id,))
                    conn.commit()
                    st.success("**La vidéo a bien été ajoutée à vos favoris!**")

                # If username already in, remove the username from fav_by_list (delete video from user's favorites)
                else:
                    fav_by_list.remove(username)
                    fav_by = ", ".join(fav_by_list)
                    c.execute("UPDATE videos SET fav_by = ? WHERE video_id = ?", (fav_by, video_id,))
                    conn.commit()
                    st.info("**La vidéo a été retirée de vos favoris!**")

        # Button to like the video
        with col_like:
            c.execute("SELECT likes, dislikes, liked_by, disliked_by FROM videos WHERE video_id = ?", (video_id,))
            result = c.fetchone()

            # Display likes number
            if result is not None:
                likes = result[0]
                st.write(f'Likes : {likes}')
            if st.button(f"\U0001F44D", key=f"like-{i}"):
                liked_by_list = liked_by.split(", ")
                disliked_by_list = disliked_by.split(", ")

                # Add one like to the video and the username to liked_by_list (if not already in)
                if username not in liked_by_list:
                    liked_by_list.append(username)
                    liked_by = ", ".join(liked_by_list)

                    # Update the database with the updated likes and liked_by_list
                    c.execute("UPDATE videos SET likes = likes + 1, liked_by = ? WHERE video_id = ?", (liked_by, video_id,))
                    conn.commit()

                    # If username had disliked this video, remove him from disliked_by_list (can either like or dislike)
                    if username in disliked_by_list:
                        disliked_by_list.remove(username)
                        disliked_by = ", ".join(disliked_by_list)
                        c.execute("UPDATE videos SET dislikes = dislikes - 1, disliked_by = ? WHERE video_id = ?",
                                  (disliked_by, video_id,))
                        conn.commit()

                # Remove the like if user already liked the video, remove him from liked_by_list and decrement likes
                else:
                    liked_by_list.remove(username)
                    liked_by = ", ".join(liked_by_list)
                    c.execute("UPDATE videos SET likes = likes - 1, liked_by = ? WHERE video_id = ?", (liked_by, video_id,))
                    conn.commit()
                st.experimental_rerun()

        # Button to dislike the video
        with col_dislike:
            c.execute("SELECT likes, dislikes, liked_by, disliked_by FROM videos WHERE video_id = ?", (video_id,))
            result = c.fetchone()

            # Display dislikes number
            if result is not None:
                dislikes = result[1]
                st.write(f'Dislikes : {dislikes}')
            if st.button(f"\U0001F44E", key=f"dislike-{i}"):
                liked_by_list = liked_by.split(", ")
                disliked_by_list = disliked_by.split(", ")

                # Add one dislike to the video and the username to disliked_by_list (if not already in)
                if username not in disliked_by_list:
                    disliked_by_list.append(username)
                    disliked_by = ", ".join(disliked_by_list)

                    # Update the database with the updated dislikes and disliked_by_list
                    c.execute("UPDATE videos SET dislikes = dislikes + 1, disliked_by = ? WHERE video_id = ?", (disliked_by, video_id,))
                    conn.commit()

                    # If username had liked this video, remove him from liked_by_list (can either like or dislike)
                    if username in liked_by_list:
                        liked_by_list.remove(username)
                        liked_by = ", ".join(liked_by_list)
                        c.execute("UPDATE videos SET likes = likes - 1, liked_by = ? WHERE video_id = ?",
                                  (liked_by, video_id,))
                        conn.commit()

                # Remove the dislike if user already disliked this video, remove him from disliked_by_list and decrement dislikes
                else:
                    disliked_by_list.remove(username)
                    disliked_by = ", ".join(disliked_by_list)
                    c.execute("UPDATE videos SET dislikes = dislikes - 1, disliked_by = ? WHERE video_id = ?", (disliked_by, video_id,))
                    conn.commit()
                st.experimental_rerun()

# Fuction to display user's favorites
def favoris():
    conn = sqlite3.connect("videos.db")
    c = conn.cursor()

    # Select all the videos where the username is in the fav_by_list
    c.execute(
        "SELECT url, title, video_id, likes, dislikes, liked_by, disliked_by, fav_by FROM videos WHERE fav_by LIKE ?",
        ('%' + username + '%',))
    rows = c.fetchall()
    st.markdown('**Liste des favoris :**')

    # Button to refresh the page and display our new favourites
    if st.button(f"Rafraichir mes favoris \U0001F504"):
        st.experimental_rerun()

    # Display the selected videos (user's favorites)
    for i, row in enumerate(reversed(rows)):
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

        # Button to remove the video from user's favorites
        if st.button(f"Retirer des favoris 	\U0000274C", key=f"remove-from-favorites-{i}"):

            #Remove the username from the video's fav_by_list
            fav_by_list = fav_by.split(", ")
            fav_by_list.remove(username)
            fav_by = ", ".join(fav_by_list)

            # Update the database with the updated fav_by_list
            c.execute("UPDATE videos SET fav_by = ? WHERE video_id = ?", (fav_by, video_id,))
            conn.commit()
            st.experimental_rerun()