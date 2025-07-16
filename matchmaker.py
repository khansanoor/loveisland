import streamlit as st
import pandas as pd
import gspread # Library for Google Sheets
import json # To parse the service account key from secrets

# --- Configuration ---
# Set the page configuration for better aesthetics
st.set_page_config(
    page_title="Love Island Matchmaker",
    page_icon="🌴",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Google Sheets Integration ---

# Function to authenticate with Google Sheets
@st.cache_resource(ttl=3600) # Cache the connection for 1 hour to avoid re-authenticating on every rerun
def get_google_sheet_client():
    """
    Authenticates with Google Sheets using service account credentials
    stored in Streamlit secrets.
    """
    try:
        # Load the service account key from Streamlit secrets
        creds = {
            "type": st.secrets["google_sheets"]["type"],
            "project_id": st.secrets["google_sheets"]["project_id"],
            "private_key_id": st.secrets["google_sheets"]["private_key_id"],
            "private_key": st.secrets["google_sheets"]["private_key"],
            "client_email": st.secrets["google_sheets"]["client_email"],
            "client_id": st.secrets["google_sheets"]["client_id"],
            "auth_uri": st.secrets["google_sheets"]["auth_uri"],
            "token_uri": st.secrets["google_sheets"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["google_sheets"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["google_sheets"]["client_x509_cert_url"],
            "universe_domain": st.secrets["google_sheets"]["universe_domain"],
        }
        gc = gspread.service_account_from_dict(creds)
        return gc
    except Exception as e:
        st.error(f"Error authenticating with Google Sheets. Make sure your `secrets.toml` is correctly configured and the service account has access to the sheet. Error: {e}")
        return None


# --- Global Variables for Google Sheet ---
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1bkrQ4q4maV0eAt4Ap4cBL5XNWvrgq0SLV3EsEcieTF4/edit?gid=0#gid=0"
WORKSHEET_NAME = "Participants" 

# --- Data Loading and Saving Functions (Needed for app to run without errors) ---
def load_participants_from_sheet():
    gc = get_google_sheet_client()
    if not gc:
        return {}
    try:
        spreadsheet = gc.open_by_url(GOOGLE_SHEET_URL)
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
        list_of_dicts = worksheet.get_all_records()
        participants_data = {item['Name']: item for item in list_of_dicts if 'Name' in item}
        return participants_data
    except gspread.exceptions.SpreadsheetNotFound:
        st.error(f"Google Sheet not found at URL: {GOOGLE_SHEET_URL}. Please check the URL.")
        return {}
    except gspread.exceptions.WorksheetNotFound:
        st.error(f"Worksheet '{WORKSHEET_NAME}' not found. Please check the worksheet name.")
        return {}
    except Exception as e:
        st.error(f"Error loading data from Google Sheet: {e}. Ensure the sheet is shared with the service account.")
        return {}

def add_participant_to_sheet(participant_answers):
    gc = get_google_sheet_client()
    if not gc:
        return False
    try:
        spreadsheet = gc.open_by_url(GOOGLE_SHEET_URL)
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
        existing_headers = worksheet.row_values(1)
        row_to_append = [participant_answers.get(header, '') for header in existing_headers]
        worksheet.append_row(row_to_append)
        return True
    except Exception as e:
        st.error(f"Error adding participant to Google Sheet: {e}")
        return False

# --- Streamlit UI (First Visible Elements) ---

st.title("🌴 Love Island Matchmaker �")
st.markdown("Welcome to the Villa! Fill out this form to get some fun insights!")

# --- Load data at the start of the app ---
# This ensures the app always has the latest data from the sheet
participants_data = load_participants_from_sheet()

# --- Participant Input Form (Step 1 Focus) ---
with st.form("participant_form", clear_on_submit=True):
    st.header("Tell Us About Yourself!")
    name = st.text_input("What is your name?", key="name_input").strip()

    st.subheader("Personality")
    intro_extro = st.radio(
        "Are you an extrovert or an introvert?",
        ["Introvert", "Extrovert", "Ambi-vert"],
        key="intro_extro_input"
    )

    submitted = st.form_submit_button("Submit My Profile!")

    # The logic for 'if submitted:' will be added in the next step (Step 2)
    # For now, this part is just to make the form visible.
    # We will expand this block in the next step.
    if submitted:
        st.info("Form submitted! (Saving data will happen in the next step)")

# --- Placeholder for the insights sections ---
# We will add these in later steps!

# --- How to Run Instructions (for your reference) ---
st.markdown("---")
st.markdown(
    """
    ### How to Run This App:

    1.  **Save the code:** Save the code above into your `matchmaker.py` file.
    2.  **Install Libraries:** If you don't have them, open your terminal or command prompt and run:
        ```bash
        pip install streamlit pandas gspread
        ```
    3.  **Google Sheet Setup (CRITICAL!):** Ensure your Google Sheet and Service Account are set up as per previous instructions.
    4.  **Run the app:** Navigate to the directory where you saved the file in your terminal and run:
        ```bash
        streamlit run matchmaker.py
        ```
    5.  **Access:** Your web browser will automatically open to the Streamlit app (usually `http://localhost:8501`).

    ### For GitHub Deployment with Streamlit Cloud:

    1.  **Ensure `matchmaker.py` is updated:** Make sure your `matchmaker.py` file in your GitHub repo has the latest code.
    2.  **Create `requirements.txt`:** In the same repository, create a file named `requirements.txt` with the following content:
        ```
        streamlit
        pandas
        gspread
        ```
    3.  **Set up Streamlit Secrets:** This is crucial for deployment. You *must* set up your Google Service Account credentials as secrets in Streamlit Cloud.
        * Go to your Streamlit Cloud app's dashboard.
        * Click on "Settings" (the three dots next to your app).
        * Go to "Secrets".
        * Add a secret named `google_sheets` and paste your service account JSON key content into it.
    4.  **Deploy:** Connect your GitHub repository to Streamlit Cloud, select `matchmaker.py` as the main file, and deploy!
    """
)
