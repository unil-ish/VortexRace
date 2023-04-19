import streamlit as st
import extra_streamlit_components as stx
import sqlite3
import mediatheque

st.set_page_config(page_title="Mes onglets", layout="wide")
with open('Visual/app/static/style.css') as f :
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.title('Vortex Race')

    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id=1, title="Profil", description="Mes informations"),
        stx.TabBarItemData(id=2, title="Statistiques", description="Mes courses"),
        stx.TabBarItemData(id=3, title="Médiathèque", description="Les vidéos"),
    ], default=1)

    if chosen_id == "1":
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            col1.header('Profil')
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

                st.write("")

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
