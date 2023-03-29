import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Chargement des données
#TROUVER DES DATASETS
images_df = pd.read_csv('data/images.csv')
videos_df = pd.read_csv('data/videos.csv')
music_df = pd.read_csv('data/music.csv')


# Interface utilisateur
st.title('Ma médiathèque')

media_type = st.selectbox('Type de média', ['Tous', 'Images', 'Vidéos', 'Musique'])

if media_type == 'Images':
    images = images_df['nom'].tolist()
    selected_image = st.selectbox('Sélectionnez une image', images)
    image = Image.open(selected_image)
    st.image(image, caption=selected_image)

elif media_type == 'Vidéos':
    videos = videos_df['nom'].tolist()
    selected_video = st.selectbox('Sélectionnez une vidéo', videos)
    st.video(selected_video)

elif media_type == 'Musique':
    music = music_df['nom'].tolist()
    selected_music = st.selectbox('Sélectionnez une musique', music)
    st.audio(selected_music)

else:
    st.write('Tous les médias')

st.sidebar.title('Recherche')
search_term = st.sidebar.text_input('Rechercher')
if search_term:
    results = []
    results += images_df[images_df['nom'].str.contains(search_term)]['nom'].tolist()
    results += videos_df[videos_df['nom'].str.contains(search_term)]['nom'].tolist()
    results += music_df[music_df['nom'].str.contains(search_term)]['nom'].tolist()
    results = list(set(results))
    st.write(f'Résultats pour "{search_term}":')
    for result in results:
        st.write(result)

st.sidebar.title('Téléchargement')
uploaded_file = st.sidebar.file_uploader('Télécharger un fichier')
if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1]
    if file_type in ['jpg', 'jpeg', 'png', 'gif']:
        images_df = images_df.append({'nom': uploaded_file.name}, ignore_index=True)
    elif file_type in ['mp4', 'avi', 'wmv', 'mov']:
        videos_df = videos_df.append({'nom':        uploaded_file.name}, ignore_index=True)
    elif file_type in ['mp3', 'wav']:
        music_df = music_df.append({'nom': uploaded_file.name}, ignore_index=True)
    else:
        st.write('Format de fichier non pris en charge')

    st.write('Fichier téléchargé avec succès.')

# Enregistrement des données
images_df.to_csv('images.csv', index=False)
videos_df.to_csv('videos.csv', index=False)
music_df.to_csv('music.csv', index=False)

