import psycopg2
import streamlit as st


def get_data_matkul_class(id_dosen):
    # Make Connection
    conn = psycopg2.connect(
        database='dashboardTA',
        user='postgres',
        password='sugianto25',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()
    
    # Execute sql
    sql = """SELECT matkul_name, tahun FROM class 
            WHERE dosen_id = %s"""
    cur.execute(sql, (id_dosen,))
    listMatkul = cur.fetchall()

    # Close sql
    cur.close()
    conn.close()

    return listMatkul 

def get_all_class():
    # Make Connection
    conn = psycopg2.connect(
        database='dashboardTA',
        user='postgres',
        password='sugianto25',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()
    
    # Execute sql
    sql = """SELECT class_id, matkul_name FROM Class"""
    cur.execute(sql)
    listMatkul = cur.fetchall()

    # Close sql
    cur.close()
    conn.close()

    return listMatkul


def check_login(username, password):
    # Make Connection
    conn = psycopg2.connect(
        database='dashboardTA',
        user='postgres',
        password='sugianto25',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()

    sql = """SELECT dosen_id FROM users WHERE username = %s AND password = %s"""
    cur.execute(sql, (username, password,))
    # Check find or not
    id = cur.fetchone()
    if id != None:
        # assign user id to session_state variable to use it on other page
        st.session_state.user_id = id
        st.success('Selamat datang dosen ID' + str(st.session_state.user_id[0]))
    else:
        st.error('User not Found!!wqe')
        
    cur.close()
    conn.close()


def input_class_cpmk(mataKuliah, semester, tahun, order, desc_values, percent_values):
    # Make Connection
    conn = psycopg2.connect(
        database='dashboardTA',
        user='postgres',
        password='sugianto25',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()

    # Query database kelas
    sql = """INSERT INTO Class(dosen_id, matkul_name, semester, class_order, tahun) Values(%s,%s,%s,%s,%s) RETURNING class_id"""
    cur.execute(sql, (st.session_state.user_id[0], mataKuliah, semester, order, tahun))
    class_id = cur.fetchone()[0]
    # Save changes
    conn.commit()

    # Query database CPMK
    sql = """INSERT INTO CPMK(class_id, number, description, percentage) Values(%s,%s,%s,%s)"""
    for i in range(len(desc_values)):
        # Input query dengan nilai yang ada
        cur.execute(sql, (class_id, i+1, desc_values[i], percent_values[i]))
        # Save changes
        conn.commit()

    # Close Connection
    cur.close()
    conn.close()

    return class_id


def get_prev_cpmk(class_id):
    # Make Connection
    conn = psycopg2.connect(
        database='dashboardTA',
        user='postgres',
        password='sugianto25',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()

    # Querying
    sql = '''SELECT number, description, percentage FROM cpmk
            WHERE class_id = %s'''
    cur.execute(sql, (class_id))
    listCPMK = cur.fetchall()

    # Close sql
    cur.close()
    conn.close()

    return listCPMK







