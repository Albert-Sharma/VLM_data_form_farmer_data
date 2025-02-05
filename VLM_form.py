import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Define categories and products
CATEGORIES = ["Fullpage", "Hybrid", "Research"]
PRODUCTS = [
    "Sava 127 FP",
    "Sava 134 FP",
    "Sava 7301",
    "Sava 7501",
    "Marshal 135",
    "Vijetha 100",
    "Sava 300 Pro",
    "Sava 300",
    "GK - KUBER",
    "SRD 88",
    "SRD-55",
    "SRD 99",
    "SRD 66",
    "Gk - NAINA",
    "GK- SHOBHA",
    "GK - SAVITHRI",
    "GK - GANGOTRI",
    "GK - CHETANA",
    "GK - PANNA",
    "S - 911"
]

st.title("मुनाफ़ा मिले जयादा - इस बार बड़े सपनों का इरादा")

conn = st.connection("gsheets", type=GSheetsConnection)

existing_data = conn.read(worksheet="Sheet1", usecols=list(range(11)), ttl=5)
existing_data = existing_data.dropna(how="all")

st.title("Farmer Registration Form")

# Initialize session states
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
    namekh_2025_acres_plan = st.number_input("NameKH 2025 Acres Plan", min_value=0.0, step=0.1)
    
    # Category selection
    selected_category = st.selectbox(
        "Category",
        options=CATEGORIES,
        key="category_selector"
    )

    # Product selection
    selected_product = st.selectbox(
        "Product",
        options=PRODUCTS,
        key="product_selector"
    )

    add_entry = st.form_submit_button("Add Entry")

    if add_entry:
        if (territory_name and tu_name and village_name and farmer_name and 
            mobile_number.isdigit() and len(mobile_number) == 10 and 
            total_paddy_acres >= 0 and selected_product):

            form_data = {
                "Territory Name": territory_name,
                "TU Name": tu_name,
                "Village Name": village_name,
                "Farmer Name": farmer_name,
                "Mobile Number": mobile_number,
                "Total Paddy Acres": total_paddy_acres,
                "Category": selected_category,
                "Product": selected_product,
                "NameKH 2025 Acres Plan": namekh_2025_acres_plan
            }

            st.session_state.entries.append(form_data)
            st.success("Entry added successfully!")
        else:
            st.error("Please fill in all fields correctly.")

# Display current entries
if st.session_state.entries:
    df_entries = pd.DataFrame(st.session_state.entries)
    st.write("Current Entries:")
    st.dataframe(df_entries)

# Submit all entries
final_submit = st.button("Submit All Entries")

if final_submit:
    if st.session_state.entries:
        df_final = pd.DataFrame(st.session_state.entries)
        update_df = pd.concat([existing_data, df_final], ignore_index=True)
        conn.update(worksheet="Sheet1", data=update_df)
        st.success("All entries submitted successfully! Please refresh the page to add more data.")
        del st.session_state.entries  # Clear entries after submission
    else:
        st.warning("No entries to submit.")