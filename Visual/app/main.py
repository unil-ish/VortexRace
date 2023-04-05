import streamlit as st
import extra_streamlit_components as stx

st.set_page_config(page_title="Mes onglets", layout="wide")
with open('Visual/app/style.css') as f :
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.title('Vortex Race')

    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id=1, title="Profil", description="Mes informations"),
        stx.TabBarItemData(id=2, title="Statistiques", description="Mes courses"),
        stx.TabBarItemData(id=3, title="Médiathèque", description="Les vidéos"),
    ], default=1)

    if chosen_id == "1":
        col1, col2, col3 = st.columns(3)
        col1.header('Profil')
        col1.checkbox('Prénom')

    if chosen_id == "2":
        col1, col2, col3 = st.columns(3)
        col2.header('Mes statistiques')
        val = stx.stepper_bar(steps=["Ready", "Get Set", "Go"])

    if chosen_id == "3":
        mediatheque.mediatheque()

if __name__ == '__main__':
    main()
