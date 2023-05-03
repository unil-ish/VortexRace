import subprocess
import json
import streamlit as st
import subprocess
from streamlit_login_auth_ui.widgets import __login__
#from streamlit_login_auth_ui.state.session_state import get as session_state_get
#import cook_book

__login__obj = __login__(auth_token = "courier_auth_token",
                    company_name = "Shims",
                    width = 200, height = 250,
                    logout_button_name = 'Logout', hide_menu_bool = False,
                    hide_footer_bool = False,
                    #lottie_url = 'https://assets8.lottiefiles.com/packages/lf20_ktwnwv5m.json'
                    )

LOGGED_IN = __login__obj.build_login_ui()


def get_logged_in_user():
    if LOGGED_IN:
        fetched_cookies = __login__obj.cookies
        if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
            loggedUser = fetched_cookies['__streamlit_login_signup_ui_username__']
            return loggedUser
        else:
            return "Username not found in cookies"
    else:
        return "User not logged in"




def get_logged_in_name(username):
    with open('_secret_auth_.json', 'r') as f:
        data = json.load(f)
    for user in data:
        if user['username'] == username:
            return user["name"]





#definit la variable
loggedUser = get_logged_in_user()
loggedName = get_logged_in_name(loggedUser)
if st.session_state['LOGGED_IN'] == True:
    st.write("Welcome, " + loggedUser + " or " + loggedName + "!")
