import streamlit as st
import extra_streamlit_components as stx
import sqlite3
import mediatheque
import logintests2
from streamlit_card import card
from streamlit_extras.chart_container import chart_container
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain
from streamlit_extras.metric_cards import style_metric_cards


username = logintests2.get_logged_in_user()

#st.set_page_config(page_title="Mes onglets", layout="wide")
with open('Visual/app/style.css') as f :
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    if username != '':
        st.title('Vortex Race')
        rain(
            emoji="🌀",
            font_size=54,
            falling_speed=5,
            animation_length="7s",
        )
        col1, col2, col3 = st.columns(3)
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
                col1.header(username)
                col1.checkbox('Prénom')
                col1.checkbox('Nom')
                col1.selectbox('Genre', ['Homme', 'Femme', 'Autres'])
                col1.metric("Cool", "10/10")
                age = col1.slider("Age", 16, 100)
                with col1.expander("Lire la suite"):
                    st.write("""
                                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                                        Mauris commodo augue ut dui malesuada, vel posuere neque tempus. 
                                        Vestibulum ut augue volutpat, gravida arcu in, eleifend nulla. 
                                        Praesent rhoncus tellus vel nunc auctor, non maximus dolor interdum. 
                                        Pellentesque quis vestibulum nisl. Sed blandit semper massa. 
                                        Etiam consequat urna id fermentum aliquet. 
                                        Integer mattis ligula sed nibh malesuada, at posuere magna bibendum. 
                                        Donec eu lectus eget quam luctus viverra in sed odio. 
                                        Suspendisse vehicula metus quis molestie commodo.
                                    """)
            with col3:
                # Afficher la liste des favoris
                conn = sqlite3.connect("videos.db")
                c = conn.cursor()
                c.execute("SELECT url, title, video_id, likes, dislikes, liked_by, disliked_by, fav_by FROM videos WHERE fav_by LIKE ?", ('%'+username+'%',))
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
                        fav_by_list.remove(username)
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
if __name__ == '__main__':
    main()
