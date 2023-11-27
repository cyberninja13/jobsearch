import streamlit as st
from jobspy.jobs import Job

def main():
    st.title("JobSpy Streamlit App")

    # Input for Job Search
    job_search = st.text_input("Enter Job Title", "Data Scientist")

    # Input for Location
    location = st.text_input("Enter Location", "New York")

    # Create Job instance with user inputs
    job = Job(job_search, location)

    # Display Job information
    st.write(f"Job Title: {job.title}")
    st.write(f"Location: {job.location}")

    # Continue with the rest of your app logic...

if __name__ == "__main__":
    main()
