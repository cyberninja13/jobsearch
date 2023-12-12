import streamlit as st
import pandas as pd

def load_data():
    file_path = "Data.xlsx"
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Set the page width outside of the main function
st.set_page_config(layout="wide")

def make_clickable(link):
    return f'<a href="{link}" target="_blank">{link}</a>'

def main():
    st.title("Job Search App")

    # Load data
    df = load_data()

    if df is not None:
        # Job Title search input
        job_title_search = st.text_input("Enter Job Title to search:", "")

        # Search button
        if st.button("Search"):
            # Filter data based on Job Title
            filtered_df = df[df["Job Title"].str.contains(job_title_search, case=False)].copy()

            # Apply clickable links to the "Link" column
            filtered_df["Link"] = filtered_df["Link"].apply(make_clickable)

            # Display the filtered data in a wider table
            st.table(filtered_df)

if __name__ == "__main__":
    main()
