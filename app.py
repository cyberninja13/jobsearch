import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from rich.table import Table
from rich.console import Console

# Function to scrape job description
@st.cache(show_spinner=False)
def scrapeJobDescription(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        jobDescription = soup.find("div", class_="show-more-less-html__markup").text.strip()
        return jobDescription
    except AttributeError:
        return ""

# Function to scrape LinkedIn jobs
@st.cache(show_spinner=False)
def scrapeLinkedin(inputJobTitle, inputJobLocation, page):
    jobs_per_page = 20
    counter = (page - 1) * jobs_per_page
    pageCounter = page

    scraped_jobs = []

    try:
        url = f"https://www.linkedin.com/jobs/search/?&keywords={inputJobTitle}&location={inputJobLocation}&refresh=true&start={counter}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        jobs = soup.select("li.jobs-search__result-item")

        for job in jobs:
            jobTitle = job.select_one("h3.base-search-card__title").text.strip()
            jobLocation = job.select_one("span.job-search-card__location").text.strip()
            jobCompany = job.select_one("h4.base-search-card__subtitle").text.strip()
            jobLink = job.select_one("a")["href"]

            jobDescription = scrapeJobDescription(jobLink)

            if jobTitle and jobLocation and jobCompany and jobLink:
                scraped_jobs.append([jobTitle, jobLocation, jobCompany, jobLink, jobDescription])

        return scraped_jobs

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []

# Streamlit UI
def main():
    st.title("LinkedIn Job Scraper")

    # Get user input using Streamlit
    inputJobTitle = st.text_input("Enter Job Title:")
    inputJobLocation = st.text_input("Enter Job Location:")

    # Get page number from user input
    page = st.number_input("Enter Page Number:", min_value=1, value=1, step=1)

    if st.button("Scrape LinkedIn"):
        scraped_jobs = scrapeLinkedin(inputJobTitle, inputJobLocation, page)

        # Display 20 jobs in a table
        if scraped_jobs:
            table = Table(show_header=True, header_style="bold")
            table.add_column("Title")
            table.add_column("Company")
            table.add_column("Location")
            table.add_column("Link")
            table.add_column("Description")

            for job in scraped_jobs:
                table.add_row(job[0], job[2], job[1], job[3], job[4][:20] + "...")

            st.write("Scraped Jobs:")
            st.table(table)

            # Save results locally using Streamlit
            if st.button("Save Results Locally"):
                df = pd.DataFrame(scraped_jobs, columns=["Title", "Company", "Location", "Link", "Description"])
                df.to_csv(f"{inputJobTitle}_{inputJobLocation}_jobs.csv", index=False)
                st.success("Results saved successfully!")

if __name__ == "__main__":
    main()
