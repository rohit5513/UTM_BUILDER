import streamlit as st
import json
import os

FILE_NAME = "campaigns.json"

DEFAULT_COUNTRIES = [
    "Global", "Austria", "Belgium", "Bulgaria", "Canada", "Denmark",
    "France", "Germany", "India", "Italy", "Luxembourg",
    "Netherlands", "Norway", "Poland", "Spain", "United Kingdom"
]

def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return {country: [] for country in DEFAULT_COUNTRIES}

def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f)

st.title("🔐 Admin Panel")

data = load_data()

# Ensure all countries exist
for c in DEFAULT_COUNTRIES:
    if c not in data:
        data[c] = []

selected_country = st.selectbox("Select Country", DEFAULT_COUNTRIES)

st.subheader(f"Campaigns for {selected_country}")

# Add campaign
new_campaign = st.text_input("Add Campaign")

if st.button("Add Campaign"):
    if new_campaign and new_campaign not in data[selected_country]:
        data[selected_country].append(new_campaign)
        save_data(data)
        st.success("Campaign added")
    else:
        st.warning("Enter unique campaign")

# Delete campaign
if data[selected_country]:
    selected_campaign = st.selectbox("Select Campaign", data[selected_country])

    if st.button("Delete Campaign"):
        data[selected_country].remove(selected_campaign)
        save_data(data)
        st.success("Deleted")
        st.rerun()
else:
    st.info("No campaigns yet")
