import streamlit as st
import psycopg2
import pandas as pd
import database_func
from streamlit_extras.switch_page_button import switch_page
from streamlit_card import card

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>Mata Kuliah Terdaftar</h1>", unsafe_allow_html=True)

# Get data from database
df = pd.DataFrame(database_func.get_data_matkul_class(st.session_state.user_id[0]))

# Check if user have matkul or not
if not df.empty:
    my_list = df[0] 

    # define the number of columns and items per container
    num_cols = 3
    items_per_container = 3

    # calculate the number of containers needed
    num_containers = len(my_list) // items_per_container
    if len(my_list) % items_per_container != 0:
        num_containers += 1

    # create a list of containers
    containers = [st.container() for _ in range(num_containers)]

    # loop over the containers and columns
    for i in range(num_containers):
        with containers[i]:
            # loop from last iteration container to last data of the next container
            # if data have less size than next container (3 column on 1 container) then we only loop until last size of data (using min func)
            for j in range(i * items_per_container, min((i + 1) * items_per_container, len(my_list))):
                col_index = j % items_per_container
                if col_index == 0:
                    col1, col2, col3 = st.columns(3)
                with locals()[f"col{col_index+1}"]:
                    if card(title=df[0].iloc[j], text=str(df[1].iloc[j])):
                        switch_page('kelas control')
        
else: #if user doesn't have matkul, give warning
    st.warning('Belum punya matkul boz')







