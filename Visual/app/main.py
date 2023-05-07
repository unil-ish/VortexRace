import streamlit as st
import extra_streamlit_components as stx
import sqlite3
import json
import mediatheque
from streamlit_login_auth_ui.widgets import __login__
from streamlit_card import card
from streamlit_extras.chart_container import chart_container
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain
from streamlit_extras.metric_cards import style_metric_cards

#st.set_page_config(page_title="Mes onglets", layout="wide")

__login__obj = __login__(auth_token = "courier_auth_token",
                    company_name = "Shims",
                    width = 200, height = 250,
                    logout_button_name = 'Logout', hide_menu_bool = False,
                    hide_footer_bool = False,
                    #lottie_url = 'https://assets8.lottiefiles.com/packages/lf20_ktwnwv5m.json'
                    )

LOGGED_IN = __login__obj.build_login_ui()

with open('Visual/app/style.css') as f :
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    if get_logged_in_user() != 'User not logged in':
        st.title('Vortex Race')
        rain(
            emoji="🌀",
            font_size=54,
            falling_speed=5,
            animation_length="0.3s",
        )
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            colored_header(
                label="My profil",
                description="All my profil informations",
                color_name="blue-80",
            )

            card(
                title="My profil",
                text="",
                image="profil.jpg",
                url="https://www.google.com",
            )
        with col2:
            colored_header(
                label="My Statistics",
                description="All your stats",
                color_name="blue-80",
            )

            card(
                title="My Statistics",
                text="",
                image="profil.jpg",
                url="https://www.google.com",
            )

            col1, col2 = st.columns(2)
            col1.metric(label="Course 1 [min]", value=12, delta=0)
            col2.metric(label="Course 2 [min]", value=15, delta=+3)
            style_metric_cards()
        with col3:
            colored_header(
                label="Médiathèque",
                description="Médiathèque",
                color_name="blue-80",
            )
            st.card(
                title="Vortex",
                text="",
                image="VortexRaceLogo.png",
            )
            card(
                title="Médiathèque",
                text="",
                image="VortexRaceLogo.png",
                #click=mediatheque.mediatheque(),
            )

        with col4:
            colored_header(
                label="Vortex Race",
                description="The Vortex Race website",
                color_name="blue-80",
            )
            card(
                title="Vortex Race",
                text="",
                image="VortexRaceLogo.png",
                url="https://www.vortexrace.ch",
            )

        #chart_data = _get_random_data()
        #with chart_container(chart_data):
            #st.write("Here's your stats")
            #st.area_chart(chart_data)

        chosen_id = stx.tab_bar(data=[
            stx.TabBarItemData(id=1, title="Profil", description="Mes informations"),
            stx.TabBarItemData(id=2, title="Statistiques", description="Mes courses"),
            stx.TabBarItemData(id=3, title="Médiathèque", description="Les vidéos"),
        ], default=1)


        if chosen_id == "1":
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
                    if st.button(f"Retirer des favoris", key=f"add-to-favorites-{i}"):
                        # Retirer la vidéo à la liste des favoris
                        fav_by_list = fav_by.split(", ")
                        fav_by_list.remove(get_logged_in_user())
                        fav_by = ", ".join(fav_by_list)
                        c.execute("UPDATE videos SET fav_by = ? WHERE video_id = ?", (fav_by, video_id,))
                        conn.commit()
                        # Rafraîchir la page
                        st.experimental_rerun()

        if chosen_id == "2":
            col1, col2, col3 = st.columns(3)
            col2.header('Mes statistiques')
            val = stx.stepper_bar(steps=["Ready", "Get Set", "Go"])

        if chosen_id == "3":
            mediatheque.mediatheque()

            # st.text_area('Bonjour')
            # st.text_input()
            # st.slider()
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
