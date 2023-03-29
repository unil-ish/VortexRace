import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import extra_streamlit_components as stx

st.set_page_config(layout="wide")

with open('Visual/app/style.css') as f :
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#image1 = st.image('/Users/thomasrywalski/Desktop/images.png', width=150, caption='Logo Vortex Race')
#stx.bouncing_image(image_source=image1, animate=True, animation_time=1500, height=100, width=300)
def main():
    st.title('Vortex Race')

    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id=1, title="Profil", description="Mes informations"),
        stx.TabBarItemData(id=2, title="Statistiques", description="Mes courses"),
        stx.TabBarItemData(id=3, title="Médiathèque", description="Les vidéos"),
    ], default=1)
    st.info(f"{chosen_id=}")

    col1, col2, col3 = st.columns(3)
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

    col2.header('Mes statistiques')
    val = stx.stepper_bar(steps=["Ready", "Get Set", "Go"])
    st.info(f"Phase #{val}")

    col3.header('Médiathèque')
    col3.checkbox('Vidéos')
    col3.checkbox('Mes vidéos')

    #st.text_area('Bonjour')
    #st.text_input()
    #st.slider()

main()