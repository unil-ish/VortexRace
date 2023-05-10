import streamlit as st
import sqlite3
import json
import mediatheque
from streamlit_login_auth_ui.widgets import __login__
from streamlit_extras.colored_header import colored_header

st.set_page_config(page_title="Mes onglets", layout="wide")

__login__obj = __login__(auth_token = "courier_auth_token",
                    company_name = "Shims",
                    width = 200, height = 250,
                    logout_button_name = 'Logout', hide_menu_bool = False,
                    hide_footer_bool = False,
                    #lottie_url = 'https://assets8.lottiefiles.com/packages/lf20_ktwnwv5m.json'
                    )

LOGGED_IN = __login__obj.build_login_ui()

def main():
    if get_logged_in_user() != 'User not logged in':
        st.title('Vortex Race')
        tab1, tab2, tab3 = st.tabs(["👤  :blue[Profil]", "📺  Médiathèque", "🌀  Vortex Race"])

        with tab1:
            colored_header(
                label="My profil",
                description="All my profil informations",
                color_name="blue-80",
            )
            col1, col2, col3 = st.columns([2, 1, 2])

            with col1:
                col1.header("Bienvenue " + get_logged_in_user() + " !")
            with col3:
                # Afficher la liste des favoris
                conn = sqlite3.connect("videos.db")
                c = conn.cursor()
                c.execute("SELECT url, title, video_id, likes, dislikes, liked_by, disliked_by, fav_by FROM videos WHERE fav_by LIKE ?", ('%'+get_logged_in_user()+'%',))
                rows = c.fetchall()
                st.write('### Liste des favoris:')
                for i, row in enumerate(reversed(rows)):
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
                    if st.button(f"Retirer des favoris", key=f"add-to-favorites-{i}-{video_id}"):
                        # Retirer la vidéo à la liste des favoris
                        fav_by_list = fav_by.split(", ")
                        fav_by_list.remove(get_logged_in_user())
                        fav_by = ", ".join(fav_by_list)
                        c.execute("UPDATE videos SET fav_by = ? WHERE video_id = ?", (fav_by, video_id,))
                        conn.commit()
                        # Rafraîchir la page
                        st.experimental_rerun()

        with tab2:
            colored_header(
                label="Médiathèque",
                description="Médiathèque",
                color_name="blue-80",
            )
            mediatheque.mediatheque()

        with tab3:
            colored_header(
                label="VortexRace",
                description="Official Website",
                color_name="blue-80",
            )

    else:
        st.warning('PLease login first')

def get_logged_in_user():
    if LOGGED_IN:
        fetched_cookies = __login__obj.cookies
        if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
            loggedUser = fetched_cookies['__streamlit_login_signup_ui_username__']
            return loggedUser
        else:
            return "Username not found in cookies"
    else:
        return "User not logged in"

def get_logged_in_name(username):
    with open('_secret_auth_.json', 'r') as f:
        data = json.load(f)
    for user in data:
        if user['username'] == username:
            return user["name"]

if __name__ == '__main__':
    main()


