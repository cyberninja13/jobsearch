import streamlit as st
import asyncio
import time
import logging
from playwright.sync_api import sync_playwright
import pandas as pd

# Configure logging to display debug information
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if 'data' not in st.session_state:
    st.session_state.data = []

def display_data():
    edited_df = st.data_editor(pd.DataFrame(st.session_state.data))

def run(playwright, max_scroll, query, browser):
    # Your run function implementation

def main():
    st.set_page_config(layout="wide")
    st.title("Search Jobs")
    positions = st.text_input("Enter comma separated position titles")
    location = st.text_input("Enter location")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col3:
        search = st.button('Search')

    if search:
        with st.spinner('Extracting data from job portals...'):
            st.session_state.data = []
            start_time = time.perf_counter()

            with sync_playwright() as p:
                p._env["WEBKIT_EXECUTABLE_PATH"] = "/usr/bin/webkitgtk"
                browser = p.webkit.launch(headless=True)
                run(p, max_scroll=3, query=f"{str(positions)} in {str(location)}", browser=browser)
                display_data()
                
                minutes = (time.perf_counter() - start_time) / 60
                logger.debug(f"Time elapsed: {round(minutes, 1)} minutes")

if __name__ == "__main__":
    main()
