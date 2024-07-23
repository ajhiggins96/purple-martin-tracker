import streamlit as st
import pandas as pd
import datetime as dt
import random

from utils import db_utils


st.set_page_config(page_title='New Nest Check', page_icon='📝')


if 'submit' not in st.session_state:
    st.session_state['submit'] = False

def submit_callback():
    """Maintain state of submit button to allow execution of 
    the overwrite/cancel buttons
    """
    st.session_state.submit = True

if 'key' not in st.session_state:
    st.session_state['key'] = 0

def clear_callback():
    """Assign a new st.data_editor key; 
    the only way to clear it is to make a new one.
    """
    st.session_state.key = random.randint(1,100000)


st.markdown("# Add a Nest Check")

with st.container():
    st.markdown("First, enter the nest check **date** and the number of available **habitats** in your colony.")
    cols = st.columns(2)
    with cols[0]:
        date = st.date_input(label='Date', value=dt.datetime.today().date())
    with cols[1]:
        habitats = st.number_input(label="Total habitats", min_value=1, value=12, step=1)


st.markdown("Then, fill in your nest check data below and click **Submit** to save.")
with st.form('obs_form'):
    template = pd.DataFrame(
        [{'date': date, 'nest': i, 'is_occupied': True, 'eggs': 0, 'young': 0} for i in range(1,habitats+1)]
    )
    config = {
        'nest': st.column_config.NumberColumn('Nest', width='small'),
        'is_occupied': st.column_config.CheckboxColumn('Occupied', width='small'),
        'eggs': st.column_config.NumberColumn('Eggs', min_value=0, max_value=12, step=1),
        'young': st.column_config.NumberColumn('Young', min_value=0, max_value=12, step=1)
    }
    user_input = st.data_editor(
        template,
        key=st.session_state.key,
        num_rows=habitats,
        column_order=['nest','is_occupied','eggs','young'],
        column_config=config,
        disabled=['nest'],
        height=35*(habitats+1)+3,
        use_container_width=True, 
        hide_index=True
    )

    submit_cols = st.columns(2)
    with submit_cols[0]:
        if st.form_submit_button('Submit', type='primary', on_click=submit_callback) or st.session_state.submit:
            # Check if date exists in db
            res = db_utils.fetch_data(f"SELECT date FROM pm_obs WHERE date='{date.strftime('%Y-%m-%d')}'")
            if res is not None: 
                st.warning(f"An observation already exists for {date}. Overwrite it?")
                overwrite_cols = st.columns(2)
                with overwrite_cols[0]:
                    if st.form_submit_button("Overwrite"):
                        # del data for date
                        db_utils.execute_query(f"DELETE FROM pm_obs WHERE date='{date}'")
                        # append to db
                        db_utils.insert_data(user_input)
                        st.session_state.submit = False
                        st.rerun()
                with overwrite_cols[1]:
                    if st.form_submit_button("Cancel", type='primary'):
                        st.session_state.submit = False
                        st.rerun()
            else:
                db_utils.insert_data(user_input)
                st.session_state.submit = False
    with submit_cols[1]:
        st.form_submit_button('Clear', on_click=clear_callback)

st.divider()

st.markdown(
    """
    #### What if I messed up?

    **I submitted incorrect data:**  
    Just resubmit the correct data for that date and choose "Overwrite".  
            
    **I got the date wrong:**  
    You can delete an entire nest check from the "My Nest Checks" page. Then submit again.
    """)
st.page_link(page='pages/3_📋_My_Nest_Checks.py', label="📋 My Nest Checks page")

# st.markdown('Database:')
# read_db = db_utils.fetch_data('SELECT * from pm_obs')
# read_db = pd.DataFrame(read_db)
# read_db

# if st.button('Delete database contents'):
#     db_utils.insert_data(query="DELETE FROM pm_obs")

db_utils.close_db()
