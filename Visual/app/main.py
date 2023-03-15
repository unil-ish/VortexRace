import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Créer un dictionnaire avec les informations d'identification
users = {
        "utilisateur1": "motdepasse1",
        "utilisateur2": "motdepasse2",
        "utilisateur3": "motdepasse3"
}

def login():
    """Fonction de connexion"""

    # Afficher le formulaire de connexion
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        # Vérifier les identifiants
        if username in users and password == users[username]:
            st.success("Vous êtes connecté !")
            return True
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect")
            return False

def create_account():
    """Fonction de création de compte"""
    # Afficher le formulaire de création de compte
    new_username = st.text_input("Nom d'utilisateur")
    new_password = st.text_input("Mot de passe", type="password")

    if st.button("Créer un compte"):
        # Ajouter les nouvelles informations d'identification au dictionnaire
        users[new_username] = new_password
        st.success("Votre compte a été créé ! Connectez-vous avec vos nouveaux identifiants.")
        return True

if __name__ == '__main__':
    st.set_page_config(page_title="Page de connexion")

    st.title("Connectez-vous")

    if create_account():
        st.info("Connectez-vous avec vos nouveaux identifiants.")

    if login():
        # Code à exécuter après la connexion réussie
        st.write("Bienvenue sur votre page d'accueil !")


df = pd.DataFrame({
    'Temps': [1, 2, 3, 4, 5],
    'Distance': [10, 20, 30, 40, 50]
})
df['Temps moyen'] = df['Distance'] / df['Temps']
fig, ax = plt.subplots()
ax.plot(df['Temps moyen'], df['Temps'])
ax.set_xlabel('Distance (km)')
ax.set_ylabel('Temps moyen (min/km)')

st.image('/Users/thomasrywalski/Desktop/images.png', width=100, caption='Logo Vortex Race')
st.title('Vortex Race')

col1, col2, col3 = st.columns(3)
col1.header('Profil')
col1.checkbox('Prénom')
col1.checkbox('Nom')

col2.header('Mes statistiques')
st.pyplot(fig)

col3.header('Médiathèque')
col3.checkbox('Vidéos')
col3.checkbox('Mes vidéos')

st.text_input('dis moi qqchose')
st.text_area('hello')
st.selectbox('profil','test')

#st.text_input()
#st.slider()