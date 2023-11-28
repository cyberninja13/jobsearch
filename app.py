# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 20:27:50 2023
@author: RDxR10
"""

import time
import csv
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import streamlit as st
from selenium import webdriver

# Function to scrape Indeed jobs
def scrape_indeed_jobs(query, location, num_pages):
    start_list = [page * 10 for page in range(num_pages)]
    base_url = 'https://in.indeed.com'
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    job_data = []
    
    for start in start_list:
        url = base_url + f'/jobs?q={query}&l={location}&start={start}'
        driver.execute_script(f"window.open('{url}', 'tab{start}');")
        time.sleep(1)
    
    for start in start_list:
        driver.switch_to.window(f'tab{start}')
    
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.find_all('td', {'class': 'resultContent'})
    
        for job in items:
            s_link = job.find('a').get('href')
            job_title = job.find('span', title=True).text.strip()
            company = job.find('span', class_='companyName').text.strip()
            location = job.find('div', class_='companyLocation').text.strip()
            if job.find('div', class_='metadata salary-snippet-container'):
                salary = job.find('div', class_='metadata salary-snippet-container').text
            elif job.find('div', class_='metadata estimated-salary-container'):
                salary = job.find('div', class_='metadata estimated-salary-container').text
            else:
                salary = ""
    
            job_link = base_url + s_link
    
            job_data.append([job_title, company, location, job_link, salary])
    
    driver.quit()
    
    return job_data

# Function to display Streamlit app
def main():
    st.title("Indeed Job Scraper")
    
    query = st.text_input("Enter job query:")
    location = st.text_input("Enter job location:")
    num_pages = st.slider("Number of pages:", 1, 10, 1)
    
    if st.button("Scrape Jobs"):
        job_data = scrape_indeed_jobs(query, location, num_pages)
        
        st.write("Scraped Job Data:")
        st.write(job_data)
        
        # Save the data to a CSV file
        filename = f'{query}_{location}_job_results.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Job Title', 'Company', 'Location', 'Job Link', 'Salary'])
            writer.writerows(job_data)
        
        st.success(f"Data saved to {filename}")

# Run the Streamlit app
if __name__ == "__main__":
    main()
