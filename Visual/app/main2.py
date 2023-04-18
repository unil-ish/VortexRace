import streamlit as st
import extra_streamlit_components as stx
from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')