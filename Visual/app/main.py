import streamlit as st
import sqlite3
import json
import mediatheque
import toml
import webbrowser
import os
from PIL import Image
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
                url = 'https://vortexrace.ch'
                if st.button("Accéder", key=3, type="primary"):
                    webbrowser.open_new_tab(url)

        with tab1:
            colored_header(
                label="My profil",
                description="",
                color_name="blue-60",
            )

            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("Mes infos")
                st.markdown("---")
                st.markdown("**Nom :**")
                st.markdown(get_logged_in_name(get_logged_in_user()))
                st.markdown("**Pseudo :**")
                st.caption("@Test2023")

                # Charger les images
                image_path1 = os.path.abspath(
                    "./Visual/app/Avatar1.jpg")
                image_path2 = os.path.abspath(
                    "./Visual/app/Avatar2.jpg")
                image_path3 = os.path.abspath(
                    "./Visual/app/Avatar3.jpg")

                avatar1 = Image.open(image_path1)
                avatar2 = Image.open(image_path2)
                avatar3 = Image.open(image_path3)

                # Créer une liste déroulante pour choisir l'avatar
                st.markdown("**Avatar :** ")
                avatar_choice = st.selectbox("Choisissez votre avatar :", ["Monstracoco", "Crocorreur", "Furieur"], format_func=lambda x: x)

                # Afficher l'avatar sélectionné
                if avatar_choice == "Monstracoco":
                    st.image(avatar1, caption="Monstracoco", use_column_width=True)
                elif avatar_choice == "Crocorreur":
                    st.image(avatar2, caption="Crocorreur", use_column_width=True)
                elif avatar_choice == "Furieur":
                    st.image(avatar3, caption="Furieur", use_column_width=True)

            with col2:
                st.subheader("Mes courses")
                st.markdown("---")
                st.markdown("**Participation :** ")
                st.markdown("3 km")
                st.markdown("**Temps :** ")
                st.markdown("12 min et 43 secondes")
                st.markdown("**Pour la prochaine édition, mes objectifs sont :**")
                st.markdown("3 km")
                st.markdown("11 min et 30 secondes")
            with col3:
                st.subheader("Mes vidéos")
                st.markdown("---")
                st.markdown("**Youtubeur préféré :** ")
                st.markdown("Elijah Green ")
                # Afficher la liste des favoris
                mediatheque.favoris()

            username = get_logged_in_user()

            # checks if the key "profile_done" exists and is false. if yes (exists and false), it indicates it to the user
            # and updates it from false to true (add button and stuff)
            if check_profile_done(username):
                st.markdown("profile is not done")
                # update_profile(username)


            # if the profile is fully finished, display message
            elif check_profile_done_finished(username):
                st.markdown("PROFILE IS DONE")
                # Afficher la liste des favoris
                # mediatheque.favoris()


            # if the key:value pair doesn't exist, create it
            else:
                add_profile_done_false(username)
                st.experimental_rerun()


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
        st.warning('Please login first')

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


def check_profile_done(username):
    """
    Checks whether a pair 'ProfileDone: false' exists in the dictionary corresponding to the given username in the JSON file.
    Returns True if it exists, and False otherwise.
    """
    with open('_secret_auth_.json', 'r') as f:
        data = json.load(f)

    for item in data:
        if item['username'] == username:
            if 'ProfileDone' in item and item['ProfileDone'] == "false":
                return True
            else:
                return False

def check_profile_done_finished(username):
    """
    Checks whether a pair 'ProfileDone: false' exists in the dictionary corresponding to the given username in the JSON file.
    Returns True if it exists, and False otherwise.
    """
    with open('_secret_auth_.json', 'r') as f:
        data = json.load(f)

    for item in data:
        if item['username'] == username:
            if 'ProfileDone' in item and item['ProfileDone'] == "true":
                return True
            else:
                return False


def add_profile_done_false(username):
    """
    Adds a new key-value pair 'ProfileDone: false' to the dictionary corresponding to the given username in the JSON file.
    """
    with open('_secret_auth_.json', 'r') as f:
        data = json.load(f)

    # Find the dictionary with the specified username
    for item in data:
        if item['username'] == username:
            item['ProfileDone'] = "false"
            break

    with open('_secret_auth_.json', 'w') as f:
        json.dump(data, f)


def update_profile(username):
    """
    Updates the 'ProfileDone' key to 'true' for the dictionary with the specified username in the list in the JSON file.
    """
    with open('_secret_auth_.json', 'r') as f:
        data = json.load(f)

    # Find the dictionary with the specified username
    for item in data:
        if item['username'] == username:
            item['ProfileDone'] = "true"
            break

    with open('_secret_auth_.json', 'w') as f:
        json.dump(data, f)



if __name__ == '__main__':
    main()


