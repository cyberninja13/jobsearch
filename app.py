import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import asyncio
from rich.progress import track
from rich.console import Console
from rich.table import Table

# Instantiate global variables
df = pd.DataFrame(columns=["Title", "Location", "Company", "Link", "Description"])
console = Console()
table = Table(show_header=True, header_style="bold")

# Function to scrape job description
async def scrapeJobDescription(url):
    global df
    driver = DriverOptions()
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    try:
        jobDescription = soup.find(
            "div", class_="show-more-less-html__markup"
        ).text.strip()
        return jobDescription
    except:
        return ""

# Function to set up WebDriver options
def DriverOptions():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    return driver

# Asynchronous function to scrape LinkedIn jobs
async def scrapeLinkedin(inputJobTitle, inputJobLocation):
    global df
    driver = DriverOptions()
    counter = 0
    pageCounter = 1
    
    while True:
        try:
            driver.get(
                f"https://www.linkedin.com/jobs/search/?&keywords={inputJobTitle}&location={inputJobLocation}&refresh=true&start={counter}"
            )

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            ulElement = soup.find("ul", class_="jobs-search__results-list")
            liElements = ulElement.find_all("li")

            for item in track(
                liElements, description=f"Linkedin - Page: {pageCounter}"
            ):
                jobTitle = item.find(
                    "h3", class_="base-search-card__title"
                ).text.strip()
                jobLocation = item.find(
                    "span", class_="job-search-card__location"
                ).text.strip()
                jobCompany = item.find(
                    "h4", class_="base-search-card__subtitle"
                ).text.strip()
                jobLink = item.find_all("a")[0]["href"]

                jobDescription = await scrapeJobDescription(jobLink)

                if jobTitle and jobLocation and jobCompany and jobLink:
                    df = pd.concat(
                        [
                            df,
                            pd.DataFrame(
                                {
                                    "Title": [jobTitle],
                                    "Location": [jobLocation],
                                    "Company": [jobCompany],
                                    "Link": [jobLink],
                                    "Description": [jobDescription],
                                }
                            ),
                        ]
                    )

            console.print("Scrape Next Page? (y/n) :", style="bold yellow", end=" ")
            continueInput = input()

            if continueInput == "n":
                break

            counter += 25
            pageCounter += 1

        except:
            break

    driver.quit()

# Asynchronous main function
async def main():
    st.title("LinkedIn Job Scraper")

    # Get user input using Streamlit
    inputJobTitle = st.text_input("Enter Job Title:")
    inputJobLocation = st.text_input("Enter Job Location:")

    if st.button("Scrape LinkedIn"):
        await scrapeLinkedin(inputJobTitle, inputJobLocation)

        # Create table using Streamlit
        st.write("Scraped Jobs:")
        st.table(df)

        # Save results locally using Streamlit
        if st.button("Save Results Locally"):
            df.to_csv(f"{inputJobTitle}_{inputJobLocation}_jobs.csv", index=False)
            st.success("Results saved successfully!")

if __name__ == "__main__":
    # Run the Streamlit app
    asyncio.run(main())
