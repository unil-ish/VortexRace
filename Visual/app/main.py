import streamlit as st
import json
import mediatheque
import webbrowser
import os
from PIL import Image
from streamlit_card import card
from streamlit_login_auth_ui.widgets import __login__
from streamlit_extras.colored_header import colored_header

st.set_page_config(
    page_title="VortexRace",
    page_icon="VortexRaceLogo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Vortex Race +")

#config = toml.load(".streamlit/config.toml")
#theme = config.get('theme', {})

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


            username = get_logged_in_user()

            # checks if the key "profile_done" exists and is false. if yes (exists and false), it indicates it to the user
            # and updates it from false to true (add button and stuff)
            if check_profile_done(username):
                update_profile(username)

                with st.form(key='profile_form'):

                    TempParticipation = st.text_input('Entrez la distance de votre course', key='temp_participation') # check box 3 ou/et 7,
                    TempTemps3km = st.text_input('Entrez le temps de votre course de 3km sous le format _minute_ _secondes_', key='temp_temps_3km')

                    TempTemps7km = st.text_input('Entrez le temps de votre course de 7km sous le format _minute_ _secondes_', key='temp_temps_7km')
                    TempObjectifDistance = st.text_input('Entrez votre objectif de course en distance', key='temp_objectif_distance')
                    TempObjectifTemps = st.text_input('Entrez votre objectif de course en temps sous le format _minute_ _secondes_', key='temp_objectif_temps')

                    TempYoutuberFavori = st.text_input('Entrez votre Youtuber favori', key='temp_youtuber_favori')
                    st.markdown("profile is not done")

                    if st.form_submit_button('Sauver'):

                        TempTemps3kmSplit = TempTemps3km.split()
                        TempTexteTemps3kmSplit = f"{TempTemps3kmSplit[0]}min {TempTemps3kmSplit[1]}secondes"
                        TempTemps7kmSplit = TempTemps7km.split()
                        TempTexteTemps7kmSplit = f"{TempTemps7kmSplit[0]}min {TempTemps7kmSplit[1]}secondes"
                        TempObjectifTempsSplit = TempObjectifTemps.split()
                        TempObjectifTempsSplit = f"{TempObjectifTempsSplit[0]}min {TempObjectifTempsSplit[1]}secondes"

                        save_profile(username, TempParticipation, TempTexteTemps3kmSplit, TempTexteTemps7kmSplit, TempObjectifDistance, TempObjectifTempsSplit, TempYoutuberFavori)
                        st.experimental_rerun()



            # if the profile is fully finished, display message
            elif check_profile_done_finished(username):
                VarParticipation, VarTemps3km, VarTemps7km, VarObjectifDistance, VarObjectifTemps, VarYoutuberFavori = get_logged_in_profile(username)
                st.markdown("PROFILE IS DONE")


                with col1:
                    st.subheader("Mes infos")
                    st.markdown("---")
                    st.markdown("**Nom :**")
                    st.markdown(get_logged_in_name(get_logged_in_user()))
                    st.markdown("**Pseudo :**")
                    st.caption(username)

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
                    avatar_choice = st.selectbox("Choisissez votre avatar :", ["Monstracoco", "Crocorreur", "Furieur"],
                                                 format_func=lambda x: x)

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
                    st.markdown(VarParticipation)
                    st.markdown("**Temps 3km:** ")
                    st.markdown(VarTemps3km)
                    st.markdown("**Temps 7km:** ")
                    st.markdown(VarTemps7km)
                    st.markdown("**Pour la prochaine édition, mes objectifs sont :**")
                    st.markdown(VarObjectifDistance)
                    st.markdown(VarObjectifTemps)

                with col3:
                    st.subheader("Mes vidéos")
                    st.markdown("---")
                    st.markdown("**Youtubeur préféré :** ")
                    st.markdown(VarYoutuberFavori)
                    # Afficher la liste des favoris
                    mediatheque.favoris()

                if st.button('Edit Profile'):
                    reset_profile(username)

                # Afficher la liste des favoris
                # mediatheque.favoris()


            # if the key:value pair doesn't exist, create it
            else:
                reset_profile(username)
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

def reset_profile(username):
    """
        Adds or resets fields to the given username in the JSON file, and adds the "profiledone" check
        """
    with open('_secret_auth_.json', 'r') as f:
        data = json.load(f)

    # Find the dictionary with the specified username
    for item in data:
        if item['username'] == username:
            item['ProfileDone'] = "false"
            item['participation'] = ""
            item['temps3kmtexte'] = ["",""]
            item['temps7kmtexte'] = ""
            item['objectifdistance'] = ""
            item['objectiftempstexte'] = ""
            item['youtuberfavori'] = ""
            break

    with open('_secret_auth_.json', 'w') as f:
        json.dump(data, f)

def save_profile(username, TempParticipation, TempTexteTemps3kmSplit, TempTexteTemps7kmSplit, TempObjectifDistance, TempObjectifTempsSplit, TempYoutuberFavori):

    """
        Completes json with the given info. CURRENTLY NOT SAVING, NOT SURE WHY
        """
    with open('_secret_auth_.json', 'r') as f:
        data = json.load(f)

    # Find the dictionary with the specified username
    for item in data:
        if item['username'] == username:
            item['ProfileDone'] = "true"
            item['participation'] = TempParticipation
            item['temps3kmtexte'] = TempTexteTemps3kmSplit
            item['temps7kmtexte'] = TempTexteTemps7kmSplit
            item['objectifdistance'] = TempObjectifDistance
            item['objectiftempstexte'] = TempObjectifTempsSplit
            item['youtuberfavori'] = TempYoutuberFavori
            break

    with open('_secret_auth_.json', 'w') as f:
        json.dump(data, f)



def get_logged_in_profile(username):
    """
    Displays the information on the profile (works if json is modified by hand)
    """
    with open('_secret_auth_.json', 'r') as f:
        data = json.load(f)
    for user in data:
        if user['username'] == username:
            VarParticipation = user['participation']
            VarTemps3km = user['temps3kmtexte']
            VarTemps7km = user['temps7kmtexte']
            VarObjectifDistance = user['objectifdistance']
            VarObjectifTemps = user['objectiftempstexte']
            VarYoutuberFavori = user['youtuberfavori']
            return VarParticipation, VarTemps3km, VarTemps7km, VarObjectifDistance, VarObjectifTemps, VarYoutuberFavori


if __name__ == '__main__':
    main()


