import streamlit as st
import sqlite3
import json
import mediatheque
import toml
import webbrowser
from streamlit_card import card
from streamlit_login_auth_ui.widgets import __login__
from streamlit_extras.colored_header import colored_header

#st.set_page_config(
    #page_title="VortexRace",
    #page_icon="VortexRaceLogo.png",
    #layout="wide",
    #initial_sidebar_state="expanded",
#)

#config = toml.load("Visual/.streamlit/config.toml")
#theme = config.get('theme', {})
#st.set_config(**theme)

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
        tab0, tab1, tab2, tab3 = st.tabs(["👋🏼  Accueil", "👤  Profil", "📺  Médiathèque", "🌀  Vortex Race"])
        with tab0:
            colored_header(
                label="Accueil",
                description="",
                color_name="blue-60",
            )
            st.markdown(" ")
            st.subheader(":blue[Bienvenue] " + get_logged_in_user() + " :blue[!]")
            st.markdown(" ")
            st.subheader(":blue[Vortex Race + est un logiciel conçu pour vous faciliter la vie!]")
            st.markdown("Avec notre web app vous pourrez rassembler toutes les vidéos qui vous intéressent pour vos entrainements,"
                        "consulter rapidement vos statistiques personnelles et accéder en un click au siteweb officiel de la Vortex Race.")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(" ")
                st.markdown(" ")
                st.subheader(":blue[Retrouvez toutes les vidéos qui vous intéresse]")
                st.markdown(" En accédant à la page médiathèque de notre web app, vous pourrez consulter toutes les vidéos qui vous plaisent"
                            " afin de rassembler les connaissances nécessaires pour vos entrainements")
                st.markdown(" ")
                url = ''
                if st.button("Accéder", key=2, type="primary"):
                    webbrowser.open_new_tab(url)

            with col2:
                card(
                    title="",
                    text="",
                    image="https://www.vid-marketing.com/wp-content/uploads/2017/05/youtube-logo2.jpg"
                )

            col1, col2 = st.columns(2)
            with col1:
                card(
                    title=" ",
                    text="",
                    url="https://vortexrace.ch",
                    image="https://vortexrace.ch/wp-content/uploads/2022/04/cropped-VortexRace_Logo_Plan-de-travail-1-copie-6.png"
                )

            with col2:
                st.markdown(" ")
                st.markdown(" ")
                st.subheader(":blue[Accéder au site web officiel de la Vortex Race]")
                st.markdown(
                    " La page Vortex Race ou bien directement avec le bouton ci-dessous, "
                    " entrez dans le monde de la mythique course et accéder par exemple à l'inscription, "
                    " la galerie photo et les informations pratiques.")
                st.markdown(" ")
                url = ''
                if st.button("Accéder", key=3, type="primary"):
                    webbrowser.open_new_tab(url)


        with tab1:
            colored_header(
                label="My profil",
                description="",
                color_name="blue-60",
            )

            # Afficher la liste des favoris
            conn = sqlite3.connect("videos.db")
            c = conn.cursor()
            c.execute("SELECT url, title, video_id, likes, dislikes, liked_by, disliked_by, fav_by FROM videos WHERE fav_by LIKE ?", ('%'+get_logged_in_user()+'%',))
            rows = c.fetchall()
            st.header('Liste des favoris:')
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
                if st.button(f"Retirer des favoris", key=f"remove-from-favorites-{i}"):
                    # Retirer la vidéo à la liste des favoris
                    fav_by_list = fav_by.split(", ")
                    fav_by_list.remove(get_logged_in_user())
                    fav_by = ", ".join(fav_by_list)
                    c.execute("UPDATE videos SET fav_by = ? WHERE video_id = ?", (fav_by, video_id,))
                    conn.commit()
                    # Rafraîchir la page
                    st.cache_data()

        with tab2:
            colored_header(
                label="Médiathèque",
                description="",
                color_name="blue-60",
            )
            mediatheque.mediatheque()

        with tab3:
            colored_header(
                label="Vortex Race",
                description="",
                color_name="blue-60",
            )
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(" ")
                st.markdown(" ")
                st.subheader(":blue[Accéder au site web officiel de la Vortex Race]")
                st.markdown(" ")
                st.markdown("Entrez dans le monde de la mythique course et accéder par exemple à l'inscription, "
                    " la galerie photo et les informations pratiques.")
                url = 'https://vortexrace.ch'
                if st.button("Accéder", key=1, type="primary"):
                    webbrowser.open_new_tab(url)

            with col2:
                card(
                    title="",
                    text="",
                    url="https://vortexrace.ch",
                    image="https://vortexrace.ch/wp-content/uploads/2022/04/cropped-VortexRace_Logo_Plan-de-travail-1-copie-6.png"
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


