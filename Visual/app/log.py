import subprocess

import streamlit as st
import subprocess
from streamlit_login_auth_ui.widgets import __login__
import main

__login__obj = __login__(auth_token = "courier_auth_token", 
                    company_name = "Shims",
                    width = 200, height = 250, 
                    logout_button_name = 'Logout', hide_menu_bool = False, 
                    hide_footer_bool = False, 
                    #lottie_url = 'https://assets8.lottiefiles.com/packages/lf20_ktwnwv5m.json'
                    )

LOGGED_IN = __login__obj.build_login_ui()

if st.session_state['LOGGED_IN'] == True:
    main.main()
    #st.markdown("Your Streamlit Application Begins here!")