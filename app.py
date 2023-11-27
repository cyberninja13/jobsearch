# /jobsearch/app.py

import streamlit as st
from jobspy.jobs import JobPost, Location, JobType
from jobspy.scrapers.indeed import IndeedScraper
from jobspy.scrapers.ziprecruiter import ZipRecruiterScraper
from jobspy.scrapers.glassdoor import GlassdoorScraper
from jobspy.scrapers.linkedin import LinkedInScraper

def main():
    st.title("JobSpy Streamlit App")

    # Input for Job Search
    job_search = st.text_input("Enter Job Title", "Data Scientist")

    # Input for Location
    location = st.text_input("Enter Location", "New York")

    # Use JobType and Location as needed
    selected_job_type = st.selectbox("Select Job Type", list(JobType))
    selected_location = st.selectbox("Select Location", list(Location))

    # Create Job instance with user inputs
    job = Job(job_search, location)

    # Scrape jobs
    scraped_jobs = scrape_jobs("indeed", job_search, location, job_type=selected_job_type)

    # Display scraped jobs
    st.dataframe(scraped_jobs)

if __name__ == "__main__":
    main()
