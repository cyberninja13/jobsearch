import streamlit as st
import pandas as pd

def load_data():
    file_path = "your_excel_file.xlsx"  # Replace with your actual file name
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def main():
    st.title("Job Search App")

    # Load data
    df = load_data()

    if df is not None:
        # Job Title search input
        job_title_search = st.text_input("Enter Job Title to search:", "")

        # Filter data based on Job Title
        filtered_df = df[df["Job Title"].str.contains(job_title_search, case=False)]

        # Display the filtered data
        st.dataframe(filtered_df)

if __name__ == "__main__":
    main()
