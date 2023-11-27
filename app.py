import streamlit as st
from jobspy.jobs import Job, Location, JobType

def main():
    st.title("JobSpy Streamlit App")

    # Input for Job Search
    job_search = st.text_input("Enter Job Title", "Data Scientist")

    # Input for Location
    location = st.text_input("Enter Location", "New York")

    # Create Job instance with user inputs
    job = Job(job_search, location)

    # Use Location and JobType as needed
    selected_location = st.selectbox("Select Location", list(Location))
    selected_job_type = st.selectbox("Select Job Type", list(JobType))

    # Continue with the rest of your app logic...

if __name__ == "__main__":
    main()
