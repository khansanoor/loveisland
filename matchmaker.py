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

