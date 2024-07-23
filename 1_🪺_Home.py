import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from utils import db_utils, plot_utils


st.set_page_config(page_title="Purple Martins", page_icon='🪶')

st.markdown("# P-Mag's Purple Martin Plots")

cols = st.columns(2)
with cols[0]:
    st.page_link(page="pages/2_📝_New_Nest_Check.py", label="Add a new nest check", icon='✏️')
with cols[1]:
    st.page_link(page="pages/3_📋_My_Nest_Checks.py", label="View my nest checks", icon='📋')

with st.container(border=True):
    years = db_utils.fetch_data("SELECT DISTINCT STRFTIME('%Y', date) FROM pm_obs ORDER BY date DESC")
    years = pd.DataFrame(years)
    year = st.radio(
        label='Select year:', 
        options=years
    )

    query = f"""
    SELECT date, SUM(is_occupied), SUM(eggs), SUM(young) FROM pm_obs
        WHERE date >= '{year}-01-01' AND date <= '{year}-12-01'
        GROUP BY date
        ORDER BY date
    """
    pm_data = db_utils.fetch_data(query)
    pm_data = pd.DataFrame(pm_data, columns=['date', 'nests', 'eggs', 'young']).set_index('date')
    pm_data.index = pd.to_datetime(pm_data.index)

    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    fig.suptitle(f'{year} Purple Martin Nest Checks')
    plot_utils.plot_line(ax[0], pm_data.eggs, y_label='Eggs')
    plot_utils.plot_line(ax[1], pm_data.young, y_label='Young')
    st.pyplot(fig)