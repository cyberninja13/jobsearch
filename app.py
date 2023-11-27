import streamlit as st
from src.jobspy import JobSpy  # Adjust the import path based on the actual structure

st.title("JobSpy Streamlit App")

# Input for Job Search
job_search = st.text_input("Enter Job Title", "Data Scientist")

# Input for Location
location = st.text_input("Enter Location", "New York")

# Create JobSpy instance with user inputs
job_spy = JobSpy(job_search, location)

# Display Results
st.write("Job Search Results:")
st.dataframe(job_spy.get_results())
