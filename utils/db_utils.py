import streamlit as st
import sqlite3


def init_db(db_file='sqlite/pm_observations.db'):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        st.error(e)

    return conn


def fetch_data(query):
    """Execute a SELECT statement"""
    conn = init_db()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    return rows if len(rows) != 0 else None


def insert_data(df):
    """Execute insert operations for each row of dataframe df."""
    conn = init_db()
    cur = conn.cursor()
    columns = ','.join(df.columns)
    values=','.join([':{:d}'.format(i+1) for i in range(len(df.columns))])
    query = f'INSERT INTO pm_obs ({columns}) VALUES ({values})'
    cur.executemany(query, df.values.tolist())
    conn.commit()
    cur.close()


def execute_query(query):
    conn = init_db()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()


def close_db():
    conn = init_db()
    conn.close()



# def load_pm_data():
#     data = {}
#     data['2024'] = {}
#     data['2024']['eggs'] = plot_utils.load_csv('static/2024_eggs.csv')
#     data['2024']['young'] = plot_utils.load_csv('static/2024_young.csv')
#     data['2024']['nests'] = plot_utils.load_csv('static/2024_nests.csv')
#     data['2023'] = {}
#     data['2023']['eggs'] = plot_utils.load_csv('static/2023_eggs.csv')
#     data['2023']['young'] = plot_utils.load_csv('static/2023_young.csv')
#     data['2023']['nests'] = plot_utils.load_csv('static/2023_nests.csv')
#     return data