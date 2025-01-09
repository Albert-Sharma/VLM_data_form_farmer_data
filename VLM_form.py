import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("मुनाफ़ा मिले जयादा - इस बार बड़े सपनों का इरादा")

conn = st.connection("gsheets", type=GSheetsConnection)

existing_data = conn.read(worksheet="Sheet1", usecols=list(range(11)), ttl=5)
existing_data = existing_data.dropna(how="all")


st.title("Farmer Registration Form")

    # Initialize a session state to hold the entries
if 'entries' not in st.session_state:
    st.session_state.entries = []

with st.form("farmer_registration"):
    territory_name = st.text_input("Territory Name")
    tu_name = st.text_input("TU Name")
    village_name = st.text_input("Village Name")
    farmer_name = st.text_input("Participating Farmer's Name")
    mobile_number = st.text_input("Mobile Number", max_chars=10)

    if mobile_number and (not mobile_number.isdigit() or len(mobile_number) != 10):
        st.error("Mobile number must be numeric and exactly 10 digits.")

    total_paddy_acres = st.number_input("Total Paddy Acres", min_value=0.0, step=0.1)
    category = st.selectbox("Category", options=["Hybrid", "Research", "Fullpage"])
    product = st.text_input("Product")
    namekh_2025_acres_plan = st.number_input("NameKH 2025 Acres Plan", min_value=0.0, step=0.1)

    add_entry = st.form_submit_button("Add Entry")

    if add_entry:
        if (territory_name and tu_name and village_name and farmer_name and 
            mobile_number.isdigit() and len(mobile_number) == 10 and 
            total_paddy_acres >= 0 and product):

            form_data = {
                "Territory Name": territory_name,
                "TU Name": tu_name,
                "Village Name": village_name,
                "Farmer Name": farmer_name,
                "Mobile Number": mobile_number,
                "Total Paddy Acres": total_paddy_acres,
                "Category": category,
                "Product": product,
                "NameKH 2025 Acres Plan": namekh_2025_acres_plan
            }

                # Append the entry to the session state entries list
            st.session_state.entries.append(form_data)
            st.success("Entry added successfully!")
        else:
            st.error("Please fill in all fields correctly.")

if st.session_state.entries:
    df_entries = pd.DataFrame(st.session_state.entries)
    st.write("Current Entries:")
    st.dataframe(df_entries)

final_submit = st.button("Submit All Entries")

if final_submit:
    if st.session_state.entries:
        df_final = pd.DataFrame(st.session_state.entries)
        update_df = pd.concat([existing_data, df_final], ignore_index=True)
        conn.update(worksheet="Sheet1", data=update_df)
        st.success("All entries submitted successfully!, Please refresh the page to add more data.")
        del st.session_state.entries  # Clear entries after submission
    else:
        st.warning("No entries to submit.")

