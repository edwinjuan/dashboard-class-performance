import streamlit as st
import random
import string
import database_func
import pandas as pd

# Initial global variable
if 'input_desc_keys' not in st.session_state:
    st.session_state.input_desc_keys= []

if 'input_percent_keys' not in st.session_state:
    st.session_state.input_percent_keys= []

if 'desc_values_prev' not in st.session_state:
    st.session_state.desc_values_prev= []

if 'percent_values_prev' not in st.session_state:
    st.session_state.percent_values_prev= []

if 'cpmk_Totpercent' not in st.session_state:
    st.session_state.cpmk_Totpercent = 100


# Start page
st.title('Data Kelas')
mataKuliah = st.text_input("Mata Kuliah:", help='Nama Mata Kuliah yang ingin ditambahkan')
col1, col2 = st.columns(2)
with col1:
    semester = st.selectbox('Semester:', ('Ganjil', 'Genap'))
with col2:
    tahun = st.text_input("Tahun: ")
order = st.text_input('Nomor kelas: ')


st.title('CPMK')

# Get all previous class data from database
listPreviousClass = database_func.get_all_class()
# Create new list to shown on selectbox
showingList = [f'{i[0]}-{i[1]}' for i in listPreviousClass]

with st.expander('Using previous CPMK'):
    with st.form('form_previous_cpmk'):
        template_class = st.selectbox('Previous CPMK:', showingList, label_visibility='collapsed')
        template_button = st.form_submit_button('Use submitted CPMK')

# Todo: Add key kedalam list sebanyak data disini
if template_button:
    template_class = template_class.split('-')[0]
    listCPMK = database_func.get_prev_cpmk(template_class)
    df = pd.DataFrame(listCPMK)
    listCPMK_size = df.shape[0]

    # Masukin key sebanyak jumlah data
    for i in range(listCPMK_size):
        st.session_state.input_desc_keys.append(random.choice(string.ascii_uppercase)+str(random.randint(0,999999)))
        st.session_state.input_percent_keys.append(random.choice(string.ascii_uppercase)+str(random.randint(0,999999)))
        st.session_state.desc_values_prev.append(df[1].iloc[i])
        st.session_state.percent_values_prev.append(df[2].iloc[i])

    

# Menempatkan container untuk menampung alert validasi
container_warning = st.empty()

col5, col6 = st.columns(2)
with col5:
    submit_button = st.button('Submit Inputed CPMK')
with col6:
    if st.button("Add new row"):
        # Menambah random key yang akan di assign ke widget input baru
        st.session_state.input_desc_keys.append(random.choice(string.ascii_uppercase)+str(random.randint(0,999999)))
        st.session_state.input_percent_keys.append(random.choice(string.ascii_uppercase)+str(random.randint(0,999999)))
        # Menambah data dummy sementara sebagai value prev CPMK
        st.session_state.desc_values_prev.append('')
        st.session_state.percent_values_prev.append(0)


placeholder = st.empty()
class_id = 0
with placeholder.container():
    # list untuk menyimpan nilai dari masing-masing widget input
    desc_values = []
    percent_values = []
    # Loop untuk membuat widget input sesuai jumlah key dan value dari load prev CPMK
    for i in range(len(st.session_state.input_desc_keys)):
        desc_value = st.text_area(f"CPMK {i+1} Description", key=st.session_state.input_desc_keys[i], value=st.session_state.desc_values_prev[i])
        desc_values.append(desc_value)
        percent_value = st.number_input("CPMK Percentage value", key=st.session_state.input_percent_keys[i], value=st.session_state.percent_values_prev[i])
        percent_values.append(percent_value)


if submit_button:
    # Check desc kosong
    isi_cpmk_full = 1
    for i in desc_values:
        if len(i) == 0:
            isi_cpmk_full = 0
            break

    # Validasi input
    if mataKuliah == '' or tahun == '' or order == '' or len(desc_values) == 0:
        container_warning.warning('Data harus diisi lengkap')
    elif not tahun.isnumeric():
        container_warning.warning('Data tahun tidak valid')
    elif isi_cpmk_full == 0:
        container_warning.warning('Deskripsi CPMK harus dilengkapi')
    elif sum(percent_values) != 100:
        container_warning.warning('Jumlah bobot belum sesuai, bobot saat ini: ' + str(sum(percent_values)))
    else:
        class_id = database_func.input_class_cpmk(mataKuliah, semester, tahun, order, desc_values, percent_values)
        container_warning.success(f'Class dan CPMK berhasil terdaftar dengan id class: {class_id}')





