# import streamlit as st
# import pandas as pd
# import gspread # Library for Google Sheets
# import json # To parse the service account key from secrets

# # --- Configuration ---
# st.set_page_config(
#     page_title="Love Island Matchmaker",
#     page_icon="🌴",
#     layout="centered",
#     initial_sidebar_state="expanded"
# )

# # --- Google Sheets Integration ---

# # Function to authenticate with Google Sheets
# @st.cache_resource(ttl=3600) # Cache the connection for 1 hour to avoid re-authenticating on every rerun
# def get_google_sheet_client():
#     """
#     Authenticates with Google Sheets using service account credentials
#     stored in Streamlit secrets.
#     """
#     try:
#         # Load the service account key from Streamlit secrets
#         creds = {
#             "type": st.secrets["google_sheets"]["type"],
#             "project_id": st.secrets["google_sheets"]["project_id"],
#             "private_key_id": st.secrets["google_sheets"]["private_key_id"],
#             "private_key": st.secrets["google_sheets"]["private_key"],
#             "client_email": st.secrets["google_sheets"]["client_email"],
#             "client_id": st.secrets["google_sheets"]["client_id"],
#             "auth_uri": st.secrets["google_sheets"]["auth_uri"],
#             "token_uri": st.secrets["google_sheets"]["token_uri"],
#             "auth_provider_x509_cert_url": st.secrets["google_sheets"]["auth_provider_x509_cert_url"],
#             "client_x509_cert_url": st.secrets["google_sheets"]["client_x509_cert_url"],
#             "universe_domain": st.secrets["google_sheets"]["universe_domain"],
#         }
#         gc = gspread.service_account_from_dict(creds)
#         return gc
#     except Exception as e:
#         st.error(f"Error authenticating with Google Sheets. Make sure your `secrets.toml` is correctly configured and the service account has access to the sheet. Error: {e}")
#         return None


# # --- Global Variables for Google Sheet ---
# GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1bkrQ4q4maV0eAt4Ap4cBL5XNWvrgq0SLV3EsEcieTF4/edit?gid=0#gid=0"
# WORKSHEET_NAME = "Participants" 

# # --- Data Loading and Saving Functions (Needed for app to run without errors) ---
# def load_participants_from_sheet():
#     gc = get_google_sheet_client()
#     if not gc:
#         return {}
#     try:
#         spreadsheet = gc.open_by_url(GOOGLE_SHEET_URL)
#         worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
#         list_of_dicts = worksheet.get_all_records()
#         participants_data = {item['Name']: item for item in list_of_dicts if 'Name' in item}
#         return participants_data
#     except gspread.exceptions.SpreadsheetNotFound:
#         st.error(f"Google Sheet not found at URL: {GOOGLE_SHEET_URL}. Please check the URL.")
#         return {}
#     except gspread.exceptions.WorksheetNotFound:
#         st.error(f"Worksheet '{WORKSHEET_NAME}' not found. Please check the worksheet name.")
#         return {}
#     except Exception as e:
#         st.error(f"Error loading data from Google Sheet: {e}. Ensure the sheet is shared with the service account.")
#         return {}

# def add_participant_to_sheet(participant_answers):
#     gc = get_google_sheet_client()
#     if not gc:
#         return False
#     try:
#         spreadsheet = gc.open_by_url(GOOGLE_SHEET_URL)
#         worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
#         existing_headers = worksheet.row_values(1)
#         row_to_append = [participant_answers.get(header, '') for header in existing_headers]
#         worksheet.append_row(row_to_append)
#         return True
#     except Exception as e:
#         st.error(f"Error adding participant to Google Sheet: {e}")
#         return False

# # --- Streamlit UI (First Visible Elements) ---

# st.title("🌴 Love Island Matchmaker 💕")
# st.markdown("Welcome to the Villa! Fill out this form to help us find you a match!")

# # --- Load data at the start of the app ---
# # This ensures the app always has the latest data from the sheet
# participants_data = load_participants_from_sheet()

# # --- Participant Input Form (Step 1 Focus) ---
# with st.form("participant_form", clear_on_submit=True):
#     # st.header("Tell Us About Yourself!")
    
# #1
#     name = st.text_input("**What is your name?**", key="name_input").strip()
    
#     #st.subheader("Personality")
# #2  
#     intro_extro = st.radio(
#         "**Are you an extrovert or an introvert?**",
#         ["Introvert", "Extrovert", "Ambi-vert"],
#         key="intro_extro_input"
#     )
# #3
#     st.image("https://raw.githubusercontent.com/khansanoor/loveisland/refs/heads/main/images/huda_dream_date.jpeg", width=100)
        
#     dream_date = st.radio(
#             "**Choose your dream date:**",
#             [
#                 "Movie night 🎬",
#                 "Mystery date 🎁",
#                 "Sunset picnic 🌅",
#                 "Bookstore browse 📚",
#                 "Explore a neighborhood 🏙️"
#             ]
#         )
    
#     submitted = st.form_submit_button("Submit My Profile!")

#     # Submitting to Gsheets
#     if submitted:
#         if not name:
#             st.error("Please enter your name to proceed!")
#         else:
#             # Prepare participant's answers as a dictionary
#             # Ensure these keys match your Google Sheet column headers exactly
#             new_participant_answers = {
#                 "Name": name,
#                 "Are you an extrovert or an introvert?": intro_extro,
#                 "Choose your dream date": dream_date,
#                 # We are not collecting Gender or Looking For yet, so they are omitted
#                 # If these columns exist in your Google Sheet, they will be filled with '' (empty string)
#             }

#             # Add to Google Sheet
#             if add_participant_to_sheet(new_participant_answers):
#                 st.success(f"Thanks, {name}! Your profile has been added to the Google Sheet.")
#                 st.balloons() # Celebrate the submission!
#                 # Reload data from sheet to include the new entry immediately
#                 # This is important for the sidebar "Show All Profiles" to update
#                 participants_data = load_participants_from_sheet()
#             else:
#                 st.error("Failed to add your profile to the Google Sheet. Please try again.")


# # --- Placeholder for the insights sections ---
# # We will add these in later steps!

# # --- Display All Islander Profiles (optional sidebar, for viewing data) ---
# # This section is kept for you to verify data is being saved and loaded.
# # It does NOT show information to other participants, only to you as the app owner/debugger.
# # st.sidebar.header("Villa Management")
# # st.sidebar.markdown("Manage participants and view profiles.")

# # if participants_data:
# #     st.sidebar.subheader("All Islander Profiles")
# #     if st.sidebar.checkbox("Show All Profiles", key="show_all_profiles_checkbox"):
# #         df = pd.DataFrame(list(participants_data.values()))
# #         st.sidebar.dataframe(df)
# # else:
# #     st.sidebar.info("No Islanders have joined the Villa yet.") 



import streamlit as st
import pandas as pd
import gspread # Library for Google Sheets
import json # To parse the service account key from secrets

# --- Configuration ---
st.set_page_config(
    page_title="Love Island Matchmaker",
    page_icon="🌴",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Mobile Optimization, Inline Image, and Font Size ---
st.markdown("""
<style>
    /* Import 'Inter' font from Google Fonts for a clean look */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

    /* Apply Inter font globally and adjust base font size for mobile */
    html, body, [class*="st-emotion"] {
        font-family: 'Inter', sans-serif;
        font-size: 0.9em; /* Slightly smaller base font size for mobile readability */
        line-height: 1.5; /* Good line spacing for readability */
    }

    /* Adjust specific heading sizes to be appropriate for mobile, relative to the new base font size */
    h1 { font-size: 2.2em; } /* Main title */
    h2 { font-size: 1.8em; }
    h3 { font-size: 1.4em; } /* Used for "Choose your dream date" */

    /* Style for the image embedded within the question text */
    .question-image {
        float: right; /* Floats the image to the right, allowing text to wrap */
        margin-left: 15px; /* Space between text and image */
        border-radius: 8px; /* Rounded corners for aesthetics */
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2); /* Subtle shadow */
        max-width: 70px; /* Ensures image doesn't get too big on larger screens */
        height: auto; /* Maintain aspect ratio */
    }

    /* Clear float after the image to prevent subsequent elements from wrapping */
    .clearfix::after {
        content: "";
        clear: both;
        display: table;
    }

    /* General styling for the form container */
    .stForm {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6; /* Light background for the form */
        box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* Soft shadow for depth */
        margin-bottom: 20px; /* Space below the form */
    }

    /* Make text input labels bold (Streamlit's internal P element within the label) */
    div[data-testid="stTextInput"] label p {
        font-weight: bold;
    }

    /* Ensure radio button labels are not excessively bold if the parent is bolded */
    div[data-testid="stRadio"] label p {
        font-weight: normal; /* Keep options readable */
    }

    /* Style for the submit button */
    .stButton > button {
        background-color: #FF69B4; /* Love Island pink */
        color: white;
        font-weight: bold;
        border-radius: 25px; /* More rounded button */
        padding: 10px 20px;
        border: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.2s ease-in-out; /* Smooth transition on hover/active */
    }

    .stButton > button:hover {
        background-color: #FF4F9D; /* Darker pink on hover */
        transform: translateY(-2px); /* Slight lift effect */
    }

</style>
""", unsafe_allow_html=True)


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

# --- Data Loading and Saving Functions ---
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

st.title("🌴 Welcome Islanders! 💕")
st.markdown("Now that you're in the villa, fill out this form to help us find you a match!")

# --- Load data at the start of the app ---
participants_data = load_participants_from_sheet()

# --- Participant Input Form ---
with st.form("participant_form", clear_on_submit=True):

    # Question 1: Name
    st.markdown("**What is your name?**")
    name = st.text_input("", key="name_input").strip()

    # Question 2: Introvert/Extrovert
    st.markdown("**Are you an extrovert or an introvert?**")
    intro_extro = st.radio(
        "",
        ["Introvert", "Extrovert", "Ambi-vert"],
        key="intro_extro_input"
    )

    # Question 3: Dream Date (Image beside question for mobile)
    # Using st.markdown with inline HTML and CSS float to achieve side-by-side layout
    st.markdown(f"""
    <div class="clearfix">
        <img src="https://raw.githubusercontent.com/khansanoor/loveisland/refs/heads/main/images/huda_dream_date.jpeg" class="question-image" width="70">
        <h3>**Choose your dream date:**</h3>
    </div>
    """, unsafe_allow_html=True)

    dream_date = st.radio(
        "", # Label is now handled by the markdown above
        [
            "Movie night 🎬",
            "Mystery date 🎁",
            "Sunset picnic 🌅",
            "Bookstore browse 📚",
            "Explore a neighborhood �️"
        ],
        key="dream_date_input"
    )

    submitted = st.form_submit_button("Submit My Profile!")

    # Submitting to Gsheets
    if submitted:
        if not name:
            st.error("Please enter your name to proceed!")
        else:
            # Prepare participant's answers as a dictionary
            # Ensure these keys match your Google Sheet column headers exactly
            new_participant_answers = {
                "Name": name,
                "Are you an extrovert or an introvert?": intro_extro,
                "Choose your dream date": dream_date, # Key matches Google Sheet column
            }

            # Add to Google Sheet
            if add_participant_to_sheet(new_participant_answers):
                st.success(f"Thanks, {name}! Your profile has been added to the Google Sheet.")
                st.balloons() # Celebrate the submission!
                # Reload data from sheet to include the new entry immediately
                participants_data = load_participants_from_sheet()
            else:
                st.error("Failed to add your profile to the Google Sheet. Please try again.")


# --- Placeholder for the insights sections ---
# This section can be expanded in later steps for matchmaking logic!

# --- Display All Islander Profiles (optional sidebar, for viewing data) ---
# This section is commented out by default as it's for debugging/admin view
# st.sidebar.header("Villa Management")
# st.sidebar.markdown("Manage participants and view profiles.")

# if participants_data:
#     st.sidebar.subheader("All Islander Profiles")
#     if st.sidebar.checkbox("Show All Profiles", key="show_all_profiles_checkbox"):
#         df = pd.DataFrame(list(participants_data.values()))
#         st.sidebar.dataframe(df)
# else:
#     st.sidebar.info("No Islanders have joined the Villa yet.")

