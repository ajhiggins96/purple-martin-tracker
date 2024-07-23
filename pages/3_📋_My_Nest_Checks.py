import streamlit as st
import pandas as pd

from utils import db_utils


st.set_page_config(page_title='My Nest Checks', page_icon='📋')

st.markdown("# My Nest Checks")

cols = st.columns([0.55,0.45])
with cols[0]:
    st.markdown("Select a row below to view that day's nest check.")

    years = db_utils.fetch_data("SELECT DISTINCT STRFTIME('%Y', date) FROM pm_obs ORDER BY date DESC")
    years = pd.DataFrame(years)
    year = st.radio(label="Year:", options=years) if len(years) > 0 else years[0]
    query = f"""
    SELECT date, SUM(is_occupied), SUM(eggs), SUM(young) FROM pm_obs
    WHERE date >= '{year}-01-01' AND date <= '{year}-12-01'
    GROUP BY date
    ORDER BY date ASC
    """
    overview = db_utils.fetch_data(query)
    overview = pd.DataFrame(overview, columns=['Date', 'Total nests', 'Total eggs', 'Total young'])
    event = st.dataframe(
        overview, 
        hide_index=True, 
        use_container_width=True, 
        height=35*(len(overview)+1)+3,
        on_select='rerun', 
        selection_mode='single-row'
    )
if len(event['selection']['rows']) == 0:
    st.info("⬆️ Select a row on the left")
else:
    selected_index = event['selection']['rows'][0]
    selected_date = overview.iloc[selected_index].loc['Date']
    query = f"""
    SELECT nest, is_occupied, eggs, young FROM pm_obs
    WHERE date = '{selected_date}'
    """
    nest_check = db_utils.fetch_data(query)
    nest_check = pd.DataFrame(nest_check, columns=['Nest', 'Occupied?', 'Eggs', 'Young'])
    with cols[0]:
        if st.button(f"Delete {selected_date}"):
            db_utils.execute_query(f"DELETE FROM pm_obs WHERE date='{selected_date}'")
            st.rerun()
    with cols[1]:
        st.markdown(f"**{pd.to_datetime(selected_date).strftime('%B %d, %Y')}**")
        st.dataframe(
            nest_check, 
            hide_index=True, 
            use_container_width=True, 
            height=35*(len(nest_check)+1)+3
        )


# st.markdown('Database:')
# read_db = db_utils.fetch_data('SELECT * from pm_obs')
# read_db = pd.DataFrame(read_db)
# read_db

# if st.button('Delete database contents'):
#     db_utils.insert_data(query="DELETE FROM pm_obs")

db_utils.close_db()
