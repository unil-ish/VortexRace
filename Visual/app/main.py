import streamlit as st
import extra_streamlit_components as stx
import sqlite3
import mediatheque
import logintests2

username = logintests2.get_logged_in_user()

#st.set_page_config(page_title="Mes onglets", layout="wide")
with open('Visual/app/style.css') as f :
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    if username != '':
        st.title('Vortex Race')

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
