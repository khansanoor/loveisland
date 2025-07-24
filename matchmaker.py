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

st.header("Welcome Islanders!🌴")
st.markdown("**Help us find a match for you in the villa ♥**")

# --- Load data at the start of the app ---
# This ensures the app always has the latest data from the sheet
participants_data = load_participants_from_sheet()

# --- Participant Input Form (Step 1 Focus) ---
with st.form("participant_form", clear_on_submit=True):
    # st.header("Tell Us About Yourself!")
    
#1
    # name = st.text_input("**❀ What is your name?**", key="name_input").strip()
    col_name, _ = st.columns([1, 3])  # Adjust the ratio to make the input narrower
    with col_name:
        name = st.text_input("**❀ What is your name?**", key="name_input").strip()

    # st.markdown("❀")
#2  
    looking_for = st.multiselect(
        "**❀ What kind of vibe are you hoping for in a match?**",
        ["Deep connection 💫", "Fun and flirty 😍", "Friendly ✌️", "Let’s see where it goes 🎲"],
        max_selections=2,
        placeholder="Pick upto 2 options 💕",
        key="match_vibe_input"
    )

    # looking_for = st.radio(
    #     "**❀ What are you looking for?**",
    #     ["Romance 💕", "Friends 🤝", "Both 💞"], index=None,

    #     key="looking_for_input"
    # )
    
#3
    st.image("https://raw.githubusercontent.com/khansanoor/loveisland/refs/heads/main/images/huda_dream_date.jpeg", width=100)
    st.caption("Huda's dream date didn't happen, but yours can!") 
    dream_date = st.radio(
            "**❀ Choose your dream date:**",
            ["Movie night 🎬",
            "Mystery date 🎁",
            "Sunset picnic 🌅",
            "Bookstore browse 📚",
            "Explore a neighborhood 🏙️"], 
            index=None,
            key="dream_date_input"
        )
#4 
    cooking_role = st.radio(
            "**❀ What role do you play when cooking with someone?**",
            ["Head Chef","Sous Chef","Adapt as needed"],
            index=None,
            key="cooking_role_input"
        )

#5
    free_day_activity = st.radio(
            "**❀ How would you spend a day with no obligations?**",
            [
                "Relax at home",
                "Go on an adventure",
                "Hang out with friends",
                "Catch up on hobbies"
            ], index=None,
            key="free_day_activity_input"
        )

#6

    intro_extro = st.radio(
            "**❀ Are you an extrovert or an introvert?**",
            ["Introvert", "Extrovert", "Ambi-vert"],
            index=None,
            key="intro_extro_input"
        )

#7
    
    morning_night = st.radio(
        "**❀ Morning person or a night owl?**",
        ["Morning 🌞", "Night 🌙", "Whenever I wake up 😴"],
        index=None,
        key="morning_night_input"
    )

#8
    personality = st.radio(
        "**❀ How would you describe yourself?**",
        ["Planner 📋", "Go with the flow 🕊", "Bit of both"],
        index=None,
        key="personality_input"
    )

#9
    recharge = st.radio(
        "**❀ How do you recharge after a long day?**",
        ["Alone time", "With friends", "Music or TV", "Journal"],
        index=None,
        key="recharge_input"
    )


#10 
    communication = st.radio(
        "**❀ Are you more of a texter or a caller?**",
        ["Text 💬", "Call 📞", "Voice notes 🎙️"],
        index=None,
        key="communication_input"
    )

#11
    vacation = st.radio(
        "**❀ What is your dream vacation?**",
        ["Beach 🏖️", "Mountains 🏔️", "Both please ✨"],
        index=None,
        key="vacation_input"
    )

#12
    favorite_meal = st.text_input(
            "**❀ What’s your favorite meal of all-time?**",
            key="favorite_meal_input"
        )
    
#13
    comfort_show = st.text_input(
        "**❀ What’s your go-to comfort show or movie?**",
        key="comfort_show_input"
    )

    
#14
    teleport_dinner = st.text_input(
        "**❀ If you could teleport anywhere for dinner tonight, where would you go?**",
        key="teleport_dinner_input"
    )

#15 
    bucket_list = st.text_input("**❀ What’s something on your bucket list?**",
        key="bucket_list_input"
    )

    
    st.caption("Last, but not least...")
#16
    st.markdown("**❀ What's your vibe in the villa?**")
    preference = st.slider(
        label="",
        min_value=0,
        max_value=10,
        value=5,
        step=1,
        format="%d",
        key="planning_style_input"
    )
    st.caption("0 = Just here for friends 🤝, 10 = Looking for romance 💘")


    submitted = st.form_submit_button("Submit My Profile!")

    if submitted:
        missing_fields = []
        if not name:
            missing_fields.append("Name")
        if not looking_for:
            missing_fields.append("What are you looking for?")
        if not dream_date:
            missing_fields.append("Dream date")
        if not cooking_role:
            missing_fields.append("Cooking Role")
        if not free_day_activity:
            missing_fields.append("Free Day Activity")
        if not intro_extro:
            missing_fields.append("Extrovert or an introvert?")
        if not morning_night:
            missing_fields.append("Morning person or a night owl?")
        if not personality:
            missing_fields.append("Planner or go-with-the-flow?")
        if not recharge:
            missing_fields.append("How do you recharge after a long day?")
        if not communication:
            missing_fields.append("Texter or a caller?")
        if not vacation:
            missing_fields.append("Dream vacation?")
        if not favorite_meal:
            missing_fields.append("Favorite Meal")
        if not comfort_show:
            missing_fields.append("Go-to comfort show or movie?")
        if not teleport_dinner:
            missing_fields.append("Teleport for dinner to")
        if not bucket_list:
            missing_fields.append("What's on your bucket list?")
        if not preference:
            missing_fields.append("Just here for friends vs looking for romance?")
    
        if missing_fields:
            st.error(f"Please fill out the following fields before submitting: {', '.join(missing_fields)}")
        else:
            new_participant_answers = {
                "Name": name,
                "What are you looking for?": ", ".join(looking_for),
                "Dream date": dream_date,
                "Cooking Role": cooking_role,
                "Free Day Activity": free_day_activity,
                "Extrovert or an introvert": intro_extro,
                "Morning person or a night owl": morning_night,
                "Planner or go-with-the-flow?": personality,
                "How do you recharge after a long day": recharge,
                "Texter or a caller": communication,
                "Dream vacation": vacation,
                "Favorite Meal": favorite_meal,
                "Go-to comfort show or movie": comfort_show,
                "Teleport for dinner to": teleport_dinner,
                "Bucket list": bucket_list,
                "Just here for friends vs looking for romance": preference,
            }
    
            if add_participant_to_sheet(new_participant_answers):
                st.success(f"Thanks, {name}! Your profile has been added to the Google Sheet.")
                st.balloons()
                participants_data = load_participants_from_sheet()
            else:
                st.error("Failed to add your profile to the Google Sheet. Please try again.")


# --- Placeholder for the insights sections ---
# We will add these in later steps!

# --- Display All Islander Profiles (optional sidebar, for viewing data) ---
# This section is kept for you to verify data is being saved and loaded.
# It does NOT show information to other participants, only to you as the app owner/debugger.
# st.sidebar.header("Villa Management")
# st.sidebar.markdown("Manage participants and view profiles.")

# if participants_data:
#     st.sidebar.subheader("All Islander Profiles")
#     if st.sidebar.checkbox("Show All Profiles", key="show_all_profiles_checkbox"):
#         df = pd.DataFrame(list(participants_data.values()))
#         st.sidebar.dataframe(df)
# else:
#     st.sidebar.info("No Islanders have joined the Villa yet.") 

