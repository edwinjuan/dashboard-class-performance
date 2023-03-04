import streamlit as st
import psycopg2
import pandas as pd
import requests
import database_func

st.session_state.cpmk_prev = False

def main():
    if 'user_id' in st.session_state:
        st.title('selamat datang dosen id '+ str(st.session_state.user_id[0]))


    with st.container():
        # Form login
        with st.form('Login'):
            username = st.text_input('Username: ')
            password = st.text_input('password: ')
            submited = st.form_submit_button()
            # Run function when button clicked
            if submited:
                database_func.check_login(username, password)
                
        
        reset_btn = st.button('Reset bozz')
        if reset_btn:
            del st.session_state.user_id




if __name__ == '__main__':
    main()

