import streamlit as st
import asyncio
import time
import logging
from playwright.sync_api import sync_playwright
import pandas as pd
from extract import run

# Configure logging to display debug information
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if 'data' not in st.session_state:
    st.session_state.data = []

def display_data() -> None:
    edited_df = st.data_editor(pd.DataFrame(st.session_state.data),
        column_order=("post_date", 
                    "title", "location", 
                    "employer", "salary",
                    "job_description",
                    "job_highlights",
                    "url"),
        column_config={
                    "post_date": "Date posted",
                    "title": "Title",
                    "location": "Location",
                    "employer": "Employer",
                    "salary": "Salary",
                    "job_description": st.column_config.TextColumn("Description", width="large"),
                    "job_highlights": st.column_config.TextColumn("Highlights", width="large"),
                    "url": st.column_config.LinkColumn("URL", width="medium")
        }
    )

def main() -> None:
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
                # Ensure headless mode
                browser = p.firefox.launch(headless=True)
                run(
                    p,
                    max_scroll=3,
                    query=f"{str(positions)} in {str(location)}",
                    browser=browser
                )
                display_data()
                minutes = (time.perf_counter() - start_time) / 60
                logger.debug(f"Time elapsed: {round(minutes, 1)} minutes")

if __name__ == "__main__":
    main()
