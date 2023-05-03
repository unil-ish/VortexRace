import streamlit as st
import extra_streamlit_components as stx
import sqlite3
import mediatheque
from streamlit_card import card
from streamlit_extras.chart_container import chart_container
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain
from streamlit_extras.metric_cards import style_metric_cards


st.set_page_config(page_title="Mes onglets", layout="wide")
with open('Visual/app/style.css') as f :
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
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
            description="This is a description",
            color_name="blue-80",
        )

        card(
            title="My profil",
            text="All my profil informations",
            image="profil.jpg",
            url="https://www.google.com",
        )
    with col2:
        colored_header(
            label="My Statistics",
            description="This is a description",
            color_name="blue-80",
        )

        card(
            title="My Statistics",
            text="All your stats",
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
            description="This is a description",
            color_name="blue-80",
        )
        card(
            title="Vortex Race",
            text="The Vortex Race website",
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

        with col3:
            # Afficher la liste des favoris
            conn = sqlite3.connect("videos.db")
            c = conn.cursor()
            c.execute("SELECT * FROM favorites")
            rows = c.fetchall()
            st.write('### Liste des favoris:')
            for i, row in enumerate(reversed(rows)):
                st.write(
                    f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{row[2]}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>',
                    unsafe_allow_html=True)
                if st.button(f"Retirer des favoris", key=f"add-to-favorites-{i}"):
                    # Retirer la vidéo à la liste des favoris
                    c.execute("DELETE FROM favorites WHERE video_id = ?", (row[2],))
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

if __name__ == '__main__':
    main()
