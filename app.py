import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from rich.table import Table
from rich.console import Console

# Instantiate global variables
df = pd.DataFrame(columns=["Title", "Location", "Company", "Link", "Description"])
console = Console()
table = Table(show_header=True, header_style="bold")

# Function to scrape job description
def scrapeJobDescription(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        jobDescription = soup.find("div", class_="show-more-less-html__markup").text.strip()
        return jobDescription
    except AttributeError:
        return ""

# Function to scrape LinkedIn jobs
def scrapeLinkedin(inputJobTitle, inputJobLocation):
    counter = 0
    pageCounter = 1

    while True:
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
                    df.loc[len(df.index)] = [jobTitle, jobLocation, jobCompany, jobLink, jobDescription]

            console.print("Scrape Next Page? (y/n) :", style="bold yellow", end=" ")
            continueInput = input()

            if continueInput == "n":
                break

            counter += 25
            pageCounter += 1

        except Exception as e:
            st.error(f"An error occurred: {e}")
            break

# Streamlit UI
def main():
    st.title("LinkedIn Job Scraper")

    # Get user input using Streamlit
    inputJobTitle = st.text_input("Enter Job Title:")
    inputJobLocation = st.text_input("Enter Job Location:")

    if st.button("Scrape LinkedIn"):
        scrapeLinkedin(inputJobTitle, inputJobLocation)

        # Create table using Streamlit
        st.write("Scraped Jobs:")
        st.table(df)

        # Save results locally using Streamlit
        if st.button("Save Results Locally"):
            df.to_csv(f"{inputJobTitle}_{inputJobLocation}_jobs.csv", index=False)
            st.success("Results saved successfully!")

if __name__ == "__main__":
    main()
