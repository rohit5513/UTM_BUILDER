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

data = load_data()

st.title("🌍 UTM Builder")

# ================= COUNTRY =================
selected_country = st.selectbox("Select Country *", DEFAULT_COUNTRIES)

# Auto website mapping
site_map = {
    "Global": "https://www.soprasteria.com/",
    "India": "https://www.soprasteria.in/"
}

base_url = st.text_input(
    "Website URL *",
    value=site_map.get(selected_country, "")
)

# ================= CAMPAIGN =================
campaigns = data.get(selected_country, [])

if campaigns:
    selected_campaign = st.selectbox("Campaign *", campaigns)
else:
    st.warning("No campaigns available")
    selected_campaign = ""

# ================= INPUT FIELDS =================
source = st.selectbox("Source *", [
    "", "LinkedIn", "Instagram", "Facebook", "X", "Youtube", "Google","Bluesky","Tiktok","Lesechos","Financialtimes","Politico","Pardot","Commerce","Ambassadeur"
])

medium = st.selectbox("Medium *", [
    "", "Search engines", "Direct traffic", "Social media", "Email marketing","Generative Ai","Webmails"
])

variant = st.selectbox("Variant *", ["", "Paid", "Organic"])

content_format = st.selectbox("Content Format *", [
    "", "Story", "Static post", "Carrousel", "Video", "Article","SingleImage","Photo","Newsletter","kakemono","broucher","qrcode"
])

identifier = st.text_input("Identifier")

st.markdown("---")

# ================= VALIDATION =================
is_valid = (
    base_url.strip() != "" and
    source != "" and
    medium != "" and
    variant != "" and
    content_format != "" and
    selected_campaign != ""
)

# ================= BUTTONS =================
col1, col2 = st.columns(2)

with col1:
    generate_clicked = st.button("🚀 Generate URL", disabled=not is_valid)

with col2:
    reset_clicked = st.button("🔄 Reset")

# ================= GENERATE =================
if generate_clicked:
    utm = (
        f"{base_url}?"
        f"utm_source={source.lower()}&"
        f"utm_medium={medium.lower().replace(' ', '_')}&"
        f"utm_campaign={selected_campaign.lower().replace(' ', '_')}&"
        f"utm_content={variant.lower()}_{content_format.lower().replace(' ', '_')}"
    )

    if identifier:
        utm += f"&utm_term={identifier}"

    st.session_state["generated_url"] = utm

# ================= RESET =================
if reset_clicked:
    st.session_state.clear()
    st.rerun()

# ================= OUTPUT =================
output = st.session_state.get(
    "generated_url",
    "Your generated URL will appear here"
)

st.code(output)
