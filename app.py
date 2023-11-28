# app.py

import streamlit as st
import pandas as pd

def main():
    st.title("Indeed Job Scraper")

    query = st.text_input("Enter job query:")
    location = st.text_input("Enter job location:")
    num_pages = st.slider("Number of pages:", 1, 10, 1)

    if st.button("Scrape Jobs"):
        # Run the web scraping script
        st.info("Scraping jobs. Please wait...")
        import scrape_indeed  # Import the scraping script
        scrape_indeed.scrape_indeed_jobs(query, location, num_pages)
        st.success("Scraping complete!")

    # Read the pre-scraped data
    filename = f'{query}_{location}_job_results.csv'
    try:
        df = pd.read_csv(filename)
        st.write("Scraped Job Data:")
        st.table(df)
    except FileNotFoundError:
        st.warning("No data available. Please scrape jobs first.")

if __name__ == "__main__":
    main()
