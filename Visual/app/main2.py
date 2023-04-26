import streamlit as st
import extra_streamlit_components as stx
import streamlit.components.v1 as components

with open('./Visual/app/style3.css') as f :
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
HtmlFile = open("./Visual/app/index3.html", 'r', encoding='utf-8')
source_code = HtmlFile.read()
#components.html(source_code)
st.markdown(source_code,unsafe_allow_html=True)


