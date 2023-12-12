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

        # Number of columns per page
        columns_per_page = 100

        # Search button
        if st.button("Search"):
            # Filter data based on Job Title
            filtered_df = df[df["A"].str.contains(job_title_search, case=False)].copy()

            # Apply clickable links to the "Link" column
            filtered_df["Link"] = filtered_df["Link"].apply(make_clickable)

            # Display the filtered data with st.dataframe and pagination
            st.dataframe(filtered_df[['A', 'B', 'C', 'Link']].head(columns_per_page), unsafe_allow_html=True)

            # Allow pagination with checkboxes
            show_additional_pages = st.checkbox("Show additional pages")
            if show_additional_pages:
                remaining_columns = filtered_df.shape[1] - columns_per_page
                num_pages = remaining_columns // columns_per_page + 1

                for page in range(1, num_pages + 1):
                    st.subheader(f"Page {page}")
                    start_idx = page * columns_per_page
                    end_idx = (page + 1) * columns_per_page
                    st.dataframe(filtered_df.iloc[:, start_idx:end_idx], unsafe_allow_html=True)

if __name__ == "__main__":
    main()
