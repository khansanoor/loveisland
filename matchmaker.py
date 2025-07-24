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
with st.form("participant_form", clear_on_submit=False):
    # st.header("Tell Us About Yourself!")
    
#1

    name = st.text_input("**❀ What is your name?**", key="name_input").strip()

    email = st.text_input("**❀ Enter your email, so we can send you your match! 📧**", key="email_input")
  
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
    love_language = st.radio(
        "**❀ What's your love language?**",
        [
            "Words that melt me 💬",
            "Physical touch 🤗",
            "Gifts 💝",
            "Quality time",
            "Do stuff for me pls"
        ],
        index=None,
        key="love_language_input"
    )

# 7. Polyamory or monogamy?
    polyamory = st.radio(
        "**❀ Polyamory or Monogamy?**",
        [
            "I’ve got love to go around 💞",
            "Maybe open to it 🤔",
            "Prefer monogamy 💍"
        ],
        index=None,
        key="polyamory_preference"
    )

#8
    islander_type = st.radio(
        "**❀ What kind of Islander are you?**",
        [
            "The heartbreaker 💔",
            "The hopeless romantic 💕",
            "The chaotic one 😈"
        ],
        index=None,
        key="islander_type_input"
    )

#9
    jealousy_response = st.radio(
        "**❀ Your match is flirting with someone else — what’s your move?**",
        [
            "Pull them for a chat 😤",
            "Give them the silent treatment 😶",
            "Flirt with someone hotter 😘",
            "Cry 😭"
        ],
        index=None,
        key="jealousy_response_input"
    )

#10
    who_to_save = st.radio(
        "**❀ Someone’s getting dumped from the island… who are you saving?**",
        [
            "My villa bestie",
            "My romantic connection",
            "The underdog 🐶",
            "Whoever’s hottest 🔥"
        ],
        index=None,
        key="who_to_save_input"
    )

#11
    dating_chaos = st.radio(
        "**❀ What kind of chaos exists in your dating history?**",
        [
            "Dated a friend's ex 👀",
            "Ghosted someone... more than once 👻",
            "Back with an ex (again) ♻️",
            "Caught in a love triangle 🔺",
            "Drama-free ✨"
        ],
        index=None,
        key="dating_chaos_input"
    )

#12
    morning_night = st.radio(
        "**❀ Morning person or a night owl?**",
        ["Morning 🌞", "Night 🌙", "Whenever I wake up 😴"],
        index=None,
        key="morning_night_input"
    )

#13
    planner = st.radio(
        "**❀ How would you describe yourself?**",
        ["Planner 📋", "Go with the flow 🕊", "Bit of both"],
        index=None,
        key="personality_input"
    )

#14
    recharge = st.radio(
        "**❀ How do you recharge after a long day?**",
        ["Alone time", "With friends", "Music or TV", "Journal"],
        index=None,
        key="recharge_input"
    )

#15
    hot_night = st.radio(
        "**❀ It's 95°, one bed, no AC — what's your play?**",
        [
            "We're sharing 🔥",
            "They’re on the couch, I need my space 🛋️",
            "Rock-paper-scissors decides ✂️"
        ],
        index=None,
        key="hot_night_input"
    )

#16
    communication = st.radio(
        "**❀ How do you text?**",
        [
            "I reply in 0.2 seconds 📲",
            "Call me instead — I hate texting ☎",
            "I leave you on read — just catch me irl",
            "I vanish for days, then send paragraphs and voice notes"
        ],
        index=None,
        key="communication_input"
    )
#17
    intro_extro = st.radio(
        "**❀ Are you an extrovert or an introvert?**",
        ["Introvert", "Extrovert", "Ambi-vert"],
        key="intro_extro_input"
    )

 #18   
    split_or_steal = st.radio(
        "**❀ Would you split the 50k or steal it?**",
        [
            "Share, of course 🥰",
            "Depends who I’m with 🤔",
            "It’s giving villain era 😈"
        ],
        index=None,
        key="split_or_steal_input"
    )


    
#19
    favorite_meal = st.text_input(
            "**❀ What’s your favorite meal of all-time?**",
            key="favorite_meal_input"
        )
    
#20
    comfort_show = st.text_input(
        "**❀ What’s your go-to comfort show or movie?**",
        key="comfort_show_input"
    )

    
#21
    teleport_dinner = st.text_input(
        "**❀ If you could teleport anywhere for dinner tonight, where would you go?**",
        key="teleport_dinner_input"
    )

#22
    bucket_list = st.text_input("**❀ What’s something on your bucket list?**",
        key="bucket_list_input"
    )

#23
    the_ick = st.text_input(
        "**❀ What’s a dealbreaker that instantly gives you the ick?**",
        key="the_ick_input"
    )
    
    st.caption("Last, but not least...")
#24
    st.markdown("**❀ What are your intentions in the villa?**")
    preference = st.slider(
        label="",
        min_value=1,
        max_value=10,
        value=5,
        step=1,
        format="%d",
        key="planning_style_input"
    )
    st.caption("1 = Just here for friends 🤝, 10 = Looking for romance 💘")


    submitted = st.form_submit_button("Submit My Profile!")

    if submitted:
        missing_fields = []
        if not name:
            missing_fields.append("Name")
        if not email:
            missing_fields.append("Email")
        if not looking_for:
            missing_fields.append("What kind of vibe are you hoping for in a match?")
        if not dream_date:
            missing_fields.append("Choose your dream date")
        if not cooking_role:
            missing_fields.append("What role do you play when cooking with someone?")
        if not free_day_activity:
            missing_fields.append("How would you spend a day with no obligations?")
        if not love_language:
            missing_fields.append("What's your love language?")
        if not polyamory:
            missing_fields.append("Polyamory or Monogamy?")
        if not islander_type:
            missing_fields.append("What kind of Islander are you?")
        if not jealousy_response:
            missing_fields.append("Your match is flirting with someone else — what’s your move?")
        if not who_to_save:
            missing_fields.append("Someone’s getting dumped — who are you saving?")
        if not dating_chaos:
            missing_fields.append("What kind of chaos exists in your dating history?")
        if not morning_night:
            missing_fields.append("Morning person or a night owl?")
        if not planner:
            missing_fields.append("How would you describe yourself?")
        if not recharge:
            missing_fields.append("How do you recharge after a long day?")
        if not hot_night:
            missing_fields.append("It's 95°, one bed, no AC — what's your play?")
        if not communication:
            missing_fields.append("How do you text?")
        if not split_or_steal:
            missing_fields.append("Would you split the 50k or steal it?")
        if not favorite_meal:
            missing_fields.append("What’s your favorite meal of all-time?")
        if not comfort_show:
            missing_fields.append("What’s your go-to comfort show or movie?")
        if not teleport_dinner:
            missing_fields.append("If you could teleport anywhere for dinner tonight, where would you go?")
        if not bucket_list:
            missing_fields.append("What’s something on your bucket list?")
        if not the_ick:
            missing_fields.append("What’s a dealbreaker that instantly gives you the ick?")
        if preference is None:
            missing_fields.append("What are your intentions in the villa?")
        
        if missing_fields:
            st.error(f"Oh no! You've forgotten to answer the following fields: {', '.join(missing_fields)}")
        else:
            new_participant_answers = {
                "Name": name,
                "Email": email,
                "What are you looking for?": ", ".join(looking_for),
                "Dream Date": dream_date,
                "Cooking Role": cooking_role,
                "Free Day Activity": free_day_activity,
                "Love Language": love_language,
                "Polyamory or Monogamy": polyamory,
                "Islander Type": islander_type,
                "Jealousy Response": jealousy_response,
                "Who Would You Save": who_to_save,
                "Dating Chaos": dating_chaos,
                "Morning vs Night": morning_night,
                "Planner": planner,
                "How You Recharge": recharge,
                "Hot Night Scenario": hot_night,
                "Communication Style": communication,
                "Extrovert or introvert": intro_extro,
                "Split or Steal": split_or_steal,
                "Favorite Meal": favorite_meal,
                "Comfort Show or Movie": comfort_show,
                "Teleport Dinner Location": teleport_dinner,
                "Bucket List Item": bucket_list,
                "Dealbreaker / Ick": the_ick,
                "Villa Intentions (1-10)": preference
            }

    
            if add_participant_to_sheet(new_participant_answers):
                st.success(f"Pack your bags {name} — you’ve made it into the villa! Your match will be revealed via email on the day of the event 💌")
                st.balloons()
                participants_data = load_participants_from_sheet()
            else:
                st.error("Failed to add you to the villa. Please reach out to organizers if the issue persists.")


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

